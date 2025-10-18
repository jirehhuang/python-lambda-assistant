# ================================
# Stage 1 — Build stage
# ================================
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

# Install system deps needed for installing and building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ curl build-essential git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=2.1.4
RUN pip install --no-cache-dir poetry==${POETRY_VERSION}

# Copy project files
COPY pyproject.toml poetry.lock ./
# Export dependencies to requirements.txt (faster install in Lambda)
RUN poetry self add poetry-plugin-export
RUN poetry export -f requirements.txt --without-hashes -o requirements.txt

# Install dependencies into a local folder (for layering)
RUN pip install --no-cache-dir --upgrade -r requirements.txt -t /opt/python

# Copy source code for later
COPY lambda_function/ lambda_function/

# ================================
# Stage 2 — Runtime stage
# ================================
FROM public.ecr.aws/lambda/python:3.12

# Copy dependencies from builder
COPY --from=builder /opt /opt

# Copy function code
COPY --from=builder /app/lambda_function ./lambda_function

# Set the Lambda handler
CMD ["lambda_function.lambda_function.lambda_handler"]
