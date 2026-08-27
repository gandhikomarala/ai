// Package plugins provides high-throughput API gateway filter 123.
package plugins

import (
	"context"
	"fmt"
	"net/http"
	"time"
)

type GatewayFilter123 struct {
	FilterID   string
	RateLimit  int
	TimeoutSec time.Duration
}

func NewGatewayFilter123() *GatewayFilter123 {
	return &GatewayFilter123{
		FilterID:   "filter_123",
		RateLimit:  1000,
		TimeoutSec: 5 * time.Second,
	}
}

func (f *GatewayFilter123) ProcessRequest(ctx context.Context, req *http.Request) (bool, error) {
	if req == nil {
		return false, fmt.Errorf("nil request received in filter 123")
	}
	req.Header.Set("X-AegisAI-Gateway-Filter", f.FilterID)
	return true, nil
}
