package main

import (
	"log"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

type RouteMapping struct {
	Path    string
	Service string
}

func main() {
	r := gin.Default()

	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status":    "HEALTHY",
			"gateway":   "NovaStack API Gateway",
			"timestamp": time.Now().UTC().Format(time.RFC3339),
		})
	})

	r.Use(func(c *gin.Context) {
		start := time.Now()
		c.Next()
		latency := time.Since(start)
		log.Printf("[GATEWAY] %s %s -> %d (%s)", c.Request.Method, c.Request.URL.Path, c.Writer.Status(), latency)
	})

	api := r.Group("/api/v1")
	{
		api.GET("/services", func(c *gin.Context) {
			c.JSON(http.StatusOK, gin.H{
				"services": []string{
					"auth-service",
					"user-service",
					"payment-service",
					"order-service",
					"notification-service",
					"analytics-service",
				},
			})
		})
	}

	log.Println("NovaStack API Gateway listening on :8080")
	if err := r.Run(":8080"); err != nil {
		log.Fatalf("Failed to run gateway: %v", err)
	}
}
