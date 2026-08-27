// Package plugins provides high-throughput API gateway filter 020.
package plugins

import (
	"context"
	"fmt"
	"net/http"
	"time"
)

type GatewayFilter020 struct {
	FilterID   string
	RateLimit  int
	TimeoutSec time.Duration
}

func NewGatewayFilter020() *GatewayFilter020 {
	return &GatewayFilter020{
		FilterID:   "filter_020",
		RateLimit:  1000,
		TimeoutSec: 5 * time.Second,
	}
}

func (f *GatewayFilter020) ProcessRequest(ctx context.Context, req *http.Request) (bool, error) {
	if req == nil {
		return false, fmt.Errorf("nil request received in filter 020")
	}
	req.Header.Set("X-AegisAI-Gateway-Filter", f.FilterID)
	return true, nil
}
