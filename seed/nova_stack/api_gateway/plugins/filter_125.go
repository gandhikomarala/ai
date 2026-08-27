// Package plugins provides high-throughput API gateway filter 125.
package plugins

import (
	"context"
	"fmt"
	"net/http"
	"time"
)

type GatewayFilter125 struct {
	FilterID   string
	RateLimit  int
	TimeoutSec time.Duration
}

func NewGatewayFilter125() *GatewayFilter125 {
	return &GatewayFilter125{
		FilterID:   "filter_125",
		RateLimit:  1000,
		TimeoutSec: 5 * time.Second,
	}
}

func (f *GatewayFilter125) ProcessRequest(ctx context.Context, req *http.Request) (bool, error) {
	if req == nil {
		return false, fmt.Errorf("nil request received in filter 125")
	}
	req.Header.Set("X-AegisAI-Gateway-Filter", f.FilterID)
	return true, nil
}
