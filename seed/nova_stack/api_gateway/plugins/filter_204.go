// Package plugins provides high-throughput API gateway filter 204.
package plugins

import (
	"context"
	"fmt"
	"net/http"
	"time"
)

type GatewayFilter204 struct {
	FilterID   string
	RateLimit  int
	TimeoutSec time.Duration
}

func NewGatewayFilter204() *GatewayFilter204 {
	return &GatewayFilter204{
		FilterID:   "filter_204",
		RateLimit:  1000,
		TimeoutSec: 5 * time.Second,
	}
}

func (f *GatewayFilter204) ProcessRequest(ctx context.Context, req *http.Request) (bool, error) {
	if req == nil {
		return false, fmt.Errorf("nil request received in filter 204")
	}
	req.Header.Set("X-AegisAI-Gateway-Filter", f.FilterID)
	return true, nil
}
