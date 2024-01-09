package main

import (
	"context"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/go-chi/render"
	"github.com/kelseyhightower/envconfig"
	"github.com/nats-io/nats.go"
	"gitlab.com/kushneryk/contextual-enigne/internal/auth"
	"gitlab.com/kushneryk/contextual-enigne/internal/handlers"
	"gitlab.com/kushneryk/contextual-enigne/internal/queue"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
	"log"
	"net/http"
	"time"
)

type Config struct {
	NatsURI      string        `envconfig:"NATS_URI"`
	RedisURI     string        `envconfig:"REDIS_URI"`
	CacheTimeout time.Duration `envconfig:"CACHE_TIMEOUT"`

	DbURL string `envconfig:"DB_URL"`

	Address string `envconfig:"ADDR"`
}

func main() {
	var cfg Config
	err := envconfig.Process("api", &cfg)
	if err != nil {
		log.Fatal(err.Error())
	}

	config := zap.NewProductionConfig()
	config.EncoderConfig.EncodeTime = zapcore.TimeEncoderOfLayout(time.RFC3339)

	l, _ := config.Build()
	defer l.Sync()
	logger := l.Sugar().With("service", "api")
	_ = context.Background()

	nc, err := nats.Connect(cfg.NatsURI)
	if err != nil {
		logger.Fatal(err)
	}

	queq := queue.New(logger, nc)

	authService := auth.New(logger)
	extractorHandler := handlers.NewExtractHandler(logger, queq, 10*time.Second)

	r := chi.NewRouter()
	r.Use(middleware.RealIP)
	r.Use(render.SetContentType(render.ContentTypeJSON))

	r.Get("/ws", extractorHandler.HandleExtractorResponse)
	r.Route("/api", func(r chi.Router) {
		r.Route("/extract", func(r chi.Router) {
			r.Use(authService.JwtAuthentication)
			r.Post("/", extractorHandler.HandleExtractorRequest)
		})
	})

	logger.Infof("app running on address: %s", cfg.Address)
	http.ListenAndServe(cfg.Address, r)
}
