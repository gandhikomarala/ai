// Package plugins provides high-throughput API gateway filter 120.
package plugins

import (
	"context"
	"fmt"
	"net/http"
	"time"
)

type GatewayFilter120 struct {
	FilterID   string
	RateLimit  int
	TimeoutSec time.Duration
}

func NewGatewayFilter120() *GatewayFilter120 {
	return &GatewayFilter120{
		FilterID:   "filter_120",
		RateLimit:  1000,
		TimeoutSec: 5 * time.Second,
	}
}

func (f *GatewayFilter120) ProcessRequest(ctx context.Context, req *http.Request) (bool, error) {
	if req == nil {
		return false, fmt.Errorf("nil request received in filter 120")
	}
	req.Header.Set("X-AegisAI-Gateway-Filter", f.FilterID)
	return true, nil
}
