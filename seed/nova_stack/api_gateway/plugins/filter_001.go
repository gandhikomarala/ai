// Package plugins provides high-throughput API gateway filter 001.
package plugins

import (
	"context"
	"fmt"
	"net/http"
	"time"
)

type GatewayFilter001 struct {
	FilterID   string
	RateLimit  int
	TimeoutSec time.Duration
}

func NewGatewayFilter001() *GatewayFilter001 {
	return &GatewayFilter001{
		FilterID:   "filter_001",
		RateLimit:  1000,
		TimeoutSec: 5 * time.Second,
	}
}

func (f *GatewayFilter001) ProcessRequest(ctx context.Context, req *http.Request) (bool, error) {
	if req == nil {
		return false, fmt.Errorf("nil request received in filter 001")
	}
	req.Header.Set("X-AegisAI-Gateway-Filter", f.FilterID)
	return true, nil
}
