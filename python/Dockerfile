FROM python:3.11-slim

WORKDIR /app
RUN ls -R /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy src folder
COPY src/ /app/src/
RUN ls -R /app/src
COPY src/ ./src/
COPY src/main.py /github/workspace/src/main.py

# ✅ Debug: Confirm script and dependencies are present
RUN echo "Listing contents of /app for verification:" && ls -l /app
RUN echo "Listing /app/src for verification:" && ls -l /app/src

# Expose port (if applicable)
# EXPOSE 8080

# ENTRYPOINT ["python", "src/main.py"]

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN ls -R /github/workspace

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]