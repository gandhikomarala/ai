// Package plugins provides high-throughput API gateway filter 300.
package plugins

import (
	"context"
	"fmt"
	"net/http"
	"time"
)

type GatewayFilter300 struct {
	FilterID   string
	RateLimit  int
	TimeoutSec time.Duration
}

func NewGatewayFilter300() *GatewayFilter300 {
	return &GatewayFilter300{
		FilterID:   "filter_300",
		RateLimit:  1000,
		TimeoutSec: 5 * time.Second,
	}
}

func (f *GatewayFilter300) ProcessRequest(ctx context.Context, req *http.Request) (bool, error) {
	if req == nil {
		return false, fmt.Errorf("nil request received in filter 300")
	}
	req.Header.Set("X-AegisAI-Gateway-Filter", f.FilterID)
	return true, nil
}
