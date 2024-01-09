package handlers

import (
	"errors"
	"fmt"
	"github.com/go-chi/render"
	"github.com/go-shiori/go-readability"
	"github.com/gorilla/websocket"
	"gitlab.com/kushneryk/contextual-enigne/internal/models"
	"go.uber.org/zap"
	"net/http"
	"regexp"
	"time"
)

var spacesRegexp = regexp.MustCompile(`\s+`)

type SuccessResponse struct {
	Message string `json:"message"`
}

func (s *SuccessResponse) Render(w http.ResponseWriter, r *http.Request) error {
	render.Status(r, http.StatusOK)
	return nil
}

func NewSuccessResponse(message string) render.Renderer {
	return &SuccessResponse{
		Message: message,
	}
}

type ErrResponse struct {
	Err            error `json:"-"` // low-level runtime error
	HTTPStatusCode int   `json:"-"` // http response status code

	StatusText string `json:"status"`          // user-level status message
	AppCode    int64  `json:"code,omitempty"`  // application-specific error code
	ErrorText  string `json:"error,omitempty"` // application-level error message, for debugging
}

func (e *ErrResponse) Render(w http.ResponseWriter, r *http.Request) error {
	render.Status(r, e.HTTPStatusCode)
	return nil
}

func ErrInvalidRequest(err error) render.Renderer {
	return &ErrResponse{
		Err:            err,
		HTTPStatusCode: 400,
		StatusText:     "Invalid request.",
		ErrorText:      err.Error(),
	}
}

type ExtractorQueue interface {
	PublishExtractorMessage(message models.ExtractorMessage) error
	ReceiveExtractorMessage(cb func(message []byte))
}

type ExtractHandler struct {
	logger         *zap.SugaredLogger
	requestTimeout time.Duration
	queue          ExtractorQueue
	upgrader       websocket.Upgrader
}

func NewExtractHandler(l *zap.SugaredLogger, q ExtractorQueue, requestTimeout time.Duration) *ExtractHandler {
	upgrader := websocket.Upgrader{
		ReadBufferSize:  1024,
		WriteBufferSize: 1024,
	}

	upgrader.CheckOrigin = func(r *http.Request) bool {
		// Allow connections from all origins
		return true
	}

	return &ExtractHandler{logger: l, queue: q, requestTimeout: requestTimeout, upgrader: upgrader}
}

func (extr *ExtractHandler) HandleExtractorRequest(w http.ResponseWriter, r *http.Request) {
	data := &models.ExtractorRequest{}
	if err := render.Bind(r, data); err != nil {
		render.Render(w, r, ErrInvalidRequest(err))
		return
	}

	article, err := readability.FromURL(data.URL, 30*time.Second)
	if err != nil {
		render.Render(w, r, ErrInvalidRequest(errors.New(fmt.Sprintf("failed to parse %s, %s\n", data.URL, err.Error()))))
		return
	}

	extractorMessage := models.ExtractorMessage{
		URL:      data.URL,
		Content:  spacesRegexp.ReplaceAllString(article.TextContent, " "),
		Title:    article.Title,
		Byline:   article.Byline,
		Length:   article.Length,
		Excerpt:  article.Excerpt,
		SiteName: article.SiteName,
		Image:    article.Image,
		Favicon:  article.Favicon,
	}

	if extractorMessage.Content == "" {
		render.Render(w, r, ErrInvalidRequest(errors.New(fmt.Sprintf("content can not be crawled from %s", data.URL))))
		return
	}

	if err = extr.queue.PublishExtractorMessage(extractorMessage); err != nil {
		render.Render(w, r, ErrInvalidRequest(errors.New(fmt.Sprintf("failed send to extractor %s, %s\n", data.URL, err.Error()))))
		return
	}

	render.Render(w, r, NewSuccessResponse("ok"))
}

func (extr *ExtractHandler) HandleExtractorResponse(w http.ResponseWriter, r *http.Request) {
	conn, err := extr.upgrader.Upgrade(w, r, nil)
	if err != nil {
		extr.logger.Info(err)
		return
	}

	extr.queue.ReceiveExtractorMessage(func(message []byte) {
		extr.logger.Info(string(message))
		err = conn.WriteMessage(websocket.TextMessage, message)
		if err != nil {
			extr.logger.Info(err)
			conn.Close()
			return
		}
	})

}
