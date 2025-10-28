# Deploying the Bengali ASR Inference Server

This guide covers deployment options for the inference server.

## Deployment Options

### 1. Hugging Face Spaces (Recommended for Quick Start)

**Pros:**
- Free GPU/CPU hosting
- Easy deployment via Git
- Built-in SSL and CDN
- Good for demos and prototyping

**Steps:**

1. Create a new Space at https://huggingface.co/new-space
   - Choose "Docker" as the SDK
   - Select hardware (CPU is free, GPU requires subscription)

2. Clone your Space repository:
```bash
git clone https://huggingface.co/spaces/<username>/bengali-asr
cd bengali-asr
```

3. Copy server files:
```bash
cp inference/server.py .
cp inference/transliterate.py .
cp inference/Dockerfile.cpu Dockerfile  # or Dockerfile.gpu for GPU
cp requirements.txt .
```

4. Create `README.md` with Space configuration:
```yaml
---
title: Bengali ASR
emoji: 🎙️
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8000
---
```

5. Upload your model:
```bash
# Use Git LFS for large files
git lfs install
git lfs track "*.bin"
git lfs track "*.pt"

# Add model files
cp -r ../models/checkpoint-best ./model

git add .
git commit -m "Initial deployment"
git push
```

6. Your API will be available at:
   - https://<username>-bengali-asr.hf.space
   - Docs: https://<username>-bengali-asr.hf.space/docs

---

### 2. Railway (Easy, Scalable)

**Pros:**
- Simple deployment from GitHub
- Automatic HTTPS
- Good free tier
- Scales automatically

**Steps:**

1. Sign up at https://railway.app

2. Create new project → Deploy from GitHub

3. Add environment variables:
   - `MODEL_PATH=/app/models/checkpoint-best`
   - `MODEL_TYPE=wav2vec2`

4. Railway will auto-detect Dockerfile and deploy

5. Add custom domain (optional) in Railway dashboard

**Cost:** 
- $5/month for 500 hours
- Additional usage-based pricing

---

### 3. Vercel (Serverless)

**Pros:**
- Excellent free tier
- Global CDN
- Serverless functions

**Cons:**
- 50MB function size limit (need to optimize model)
- 10s timeout on free tier

**Steps:**

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Create `vercel.json`:
```json
{
  "builds": [
    {
      "src": "inference/server.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "inference/server.py"
    }
  ]
}
```

3. Deploy:
```bash
vercel --prod
```

**Note:** For Vercel, you'll need to:
- Use ONNX quantized model (smaller size)
- Or host model externally (S3, Hugging Face Hub)

---

### 4. Google Cloud Platform (Production Grade)

**Pros:**
- Full control
- GPU support
- Excellent reliability
- Global infrastructure

**Deployment on Cloud Run:**

1. Install Google Cloud SDK:
```bash
# macOS
brew install google-cloud-sdk

# Login
gcloud auth login
gcloud config set project <PROJECT_ID>
```

2. Build and push Docker image:
```bash
cd inference

# Build
gcloud builds submit --tag gcr.io/<PROJECT_ID>/bengali-asr:latest

# Or with GPU
gcloud builds submit -f Dockerfile.gpu --tag gcr.io/<PROJECT_ID>/bengali-asr-gpu:latest
```

3. Deploy to Cloud Run:
```bash
# CPU deployment
gcloud run deploy bengali-asr \
  --image gcr.io/<PROJECT_ID>/bengali-asr:latest \
  --platform managed \
  --region us-central1 \
  --memory 4Gi \
  --cpu 2 \
  --allow-unauthenticated \
  --max-instances 10

# Get the URL
gcloud run services describe bengali-asr --region us-central1 --format 'value(status.url)'
```

**For GPU (Cloud Run doesn't support GPU, use GKE):**

```bash
# Create GKE cluster with GPU nodes
gcloud container clusters create bengali-asr-cluster \
  --zone us-central1-a \
  --machine-type n1-standard-4 \
  --accelerator type=nvidia-tesla-t4,count=1 \
  --num-nodes 1

# Deploy with kubectl
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

**Cost Estimate:**
- Cloud Run: ~$0.10/day with minimal traffic
- GKE with GPU: ~$300/month

---

### 5. AWS (ECS or Lambda)

**Option A: AWS Lambda + API Gateway**

1. Use AWS SAM for deployment:
```bash
# Install SAM CLI
brew install aws-sam-cli

# Create template.yaml
# Deploy
sam build
sam deploy --guided
```

**Option B: ECS with Fargate**

1. Create ECR repository:
```bash
aws ecr create-repository --repository-name bengali-asr
```

2. Build and push:
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

docker build -f Dockerfile.cpu -t bengali-asr .
docker tag bengali-asr:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/bengali-asr:latest
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/bengali-asr:latest
```

3. Create ECS task and service via AWS Console or Terraform

---

### 6. Self-Hosted (Your Own Server)

**Requirements:**
- Ubuntu 20.04+ server
- (Optional) NVIDIA GPU for faster inference
- Domain name with SSL certificate

**Setup:**

1. Install Docker:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# For GPU support
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

2. Clone repository:
```bash
git clone https://github.com/BRAC/bengali-dialect-transcription.git
cd bengali-dialect-transcription
```

3. Build and run:
```bash
# CPU
cd inference
docker-compose -f docker-compose.cpu.yml up -d

# GPU
docker-compose -f docker-compose.gpu.yml up -d
```

4. Set up NGINX reverse proxy:
```bash
sudo apt install nginx certbot python3-certbot-nginx

# Create NGINX config
sudo nano /etc/nginx/sites-available/bengali-asr
```

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/bengali-asr /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com
```

5. Set up systemd service for auto-restart:
```bash
sudo nano /etc/systemd/system/bengali-asr.service
```

```ini
[Unit]
Description=Bengali ASR Service
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/path/to/bengali-dialect-transcription/inference
ExecStart=/usr/bin/docker-compose -f docker-compose.cpu.yml up -d
ExecStop=/usr/bin/docker-compose -f docker-compose.cpu.yml down

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable bengali-asr
sudo systemctl start bengali-asr
```

---

## Monitoring & Maintenance

### Health Checks

All deployment options should implement:
- `/health` endpoint monitoring
- Log aggregation (CloudWatch, Stackdriver, etc.)
- Alerts on errors or high latency

### Scaling Considerations

1. **Horizontal Scaling:**
   - Use load balancer (AWS ALB, GCP Load Balancer, NGINX)
   - Session affinity not required (stateless API)

2. **Model Optimization:**
   - Use ONNX quantization for CPU
   - TensorRT for GPU
   - Model distillation for smaller models

3. **Caching:**
   - Cache common transcriptions (Redis)
   - CDN for static assets

---

## Cost Comparison

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| Hugging Face Spaces | CPU unlimited | GPU: $0.60/hr | Demos, prototypes |
| Railway | $5 credit | $5/month + usage | Small-medium projects |
| Vercel | 100GB-hrs/mo | $20/month | Serverless, global CDN |
| GCP Cloud Run | 2M requests/mo | Pay-per-use | Production, auto-scale |
| AWS Lambda | 1M requests/mo | Pay-per-use | Event-driven |
| Self-hosted | N/A | Server cost | Full control, sensitive data |

---

## Security Checklist

- [ ] Enable HTTPS/SSL
- [ ] Implement rate limiting
- [ ] Add authentication (API keys, JWT)
- [ ] Sanitize file uploads
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Monitor for abuse
- [ ] CORS configuration
- [ ] Environment variable protection

---

## Support

For deployment issues, contact:
- Email: [TODO: Add support email]
- GitHub Issues: https://github.com/BRAC/bengali-dialect-transcription/issues

---

*Last Updated: October 29, 2025*
