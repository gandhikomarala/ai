import express, { Request, Response } from "express";
import jwt from "jsonwebtoken";

const app = express();
app.use(express.json());

const JWT_SECRET = process.env.JWT_SECRET || "novastack-auth-secret-key-12345";

interface UserPayload {
  userId: string;
  email: string;
  role: string;
  orgId: string;
}

app.get("/health", (req: Request, res: Response) => {
  res.json({ status: "HEALTHY", service: "auth-service", timestamp: new Date().toISOString() });
});

app.post("/auth/token", (req: Request, res: Response) => {
  const { email, password } = req.body;
  if (!email || !password) {
    return res.status(400).json({ error: "Missing email or password" });
  }
  
  const token = jwt.sign(
    { userId: "usr_9988", email, role: "ENGINEER", orgId: "org_novastack" },
    JWT_SECRET,
    { expiresIn: "1h" }
  );

  return res.json({
    accessToken: token,
    tokenType: "Bearer",
    expiresIn: 3600
  });
});

app.post("/auth/verify", (req: Request, res: Response) => {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    return res.status(401).json({ valid: false, error: "Missing Bearer token" });
  }

  const token = authHeader.split(" ")[1];
  try {
    const decoded = jwt.verify(token, JWT_SECRET) as UserPayload;
    return res.json({ valid: true, user: decoded });
  } catch (err) {
    return res.status(401).json({ valid: false, error: "Invalid or expired token" });
  }
});

const PORT = process.env.PORT || 8081;
app.listen(PORT, () => {
  console.log(`NovaStack Auth Service running on port ${PORT}`);
});
