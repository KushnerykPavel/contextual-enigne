package queue

import (
	"encoding/json"
	"fmt"
	"github.com/nats-io/nats.go"
	"gitlab.com/kushneryk/contextual-enigne/internal/models"
	"go.uber.org/zap"
)

type Queue struct {
	logger *zap.SugaredLogger
	conn   *nats.Conn
}

func New(l *zap.SugaredLogger, c *nats.Conn) *Queue {
	return &Queue{
		logger: l.With("module", "queue"),
		conn:   c,
	}
}

func (q *Queue) PublishExtractorMessage(message models.ExtractorMessage) error {
	body, err := json.Marshal(message)
	if err != nil {
		return fmt.Errorf("marshal.message.error: %w", err)
	}
	q.logger.With("message", string(body)).Info("contextual-engine-message")
	return q.conn.Publish("contextual-engine-extractor", body)
}

func (q *Queue) ReceiveExtractorMessage(cb func(message []byte)) {
	q.conn.Subscribe("contextual-engine-extractor-response", func(m *nats.Msg) {
		cb(m.Data)
		m.Ack()
	})
}
