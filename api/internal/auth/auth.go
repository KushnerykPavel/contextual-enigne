package auth

import (
	"context"
	"errors"
	"fmt"
	"go.uber.org/zap"
	"net/http"
	"strings"
)

type Service struct {
	logger *zap.SugaredLogger
}

func New(l *zap.SugaredLogger) *Service {
	return &Service{logger: l.With("service", "auth")}
}

func (s *Service) JwtAuthentication(next http.Handler) http.Handler {
	logger := s.logger.With("operation", "JwtAuthentication")
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {

		notAuth := []string{"/api/users/login", "/api/users/register"} //List of endpoints that doesn't require auth
		requestPath := r.URL.Path                                      //current request path

		//check if request does not need authentication, serve the request if it doesn't need it
		for _, value := range notAuth {
			if value == requestPath {
				next.ServeHTTP(w, r)
				return
			}
		}

		userID, err := s.getUserIdFromToken(r)
		if err != nil {
			logger.Info(err.Error())
			w.WriteHeader(http.StatusForbidden)
			w.Header().Add("Content-Type", "application/json")
			return
		}

		ctx := context.WithValue(r.Context(), "id", userID)
		r = r.WithContext(ctx)
		next.ServeHTTP(w, r) //proceed in the middleware chain!
	})
}

func (s *Service) getUserIdFromToken(r *http.Request) (int, error) {
	tokenHeader := r.Header.Get("Authorization") //Grab the token from the header

	if tokenHeader == "" { //Token is missing, returns with error code 403 Unauthorized
		return 0, errors.New("unauthorized request")
	}

	splitted := strings.Split(tokenHeader, " ") //The token normally comes in format `Bearer {token-body}`, we check if the retrieved token matched this requirement
	if len(splitted) != 2 {
		return 0, errors.New(fmt.Sprintf("incorrect token header %s", tokenHeader))
	}

	token := splitted[1]
	if token != "demo" {
		return 0, errors.New(fmt.Sprintf("incorrect token name %s", token))
	}

	return 0, nil
}
