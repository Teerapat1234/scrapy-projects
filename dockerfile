FROM python:3.13.2-slim

# Define the non-root user that n8n will use
ENV SSH_USER=n8n_user
ENV SSH_HOME=/home/$SSH_USER

# Switch to root user to install system packages and SSH
USER root

# 1. Install OpenSSH server, client, and bash
RUN apt-get update && \
    apt-get install -y --no-install-recommends openssh-server openssh-client bash && \
    rm -rf /var/cache/apt/lists/*

# 2. Setup SSH configuration for key-based authentication
# Create the SSH server directory and host keys
RUN mkdir -p /var/run/sshd && \
    ssh-keygen -A 

# Create the non-root user (no password set)
RUN useradd -m -s /bin/bash ${SSH_USER}

# Create .ssh directory and set ownership
RUN mkdir -p $SSH_HOME/.ssh && \
    chown -R $SSH_USER:$SSH_USER $SSH_HOME

# *IMPORTANT Copy the public key for authorized access
COPY n8n_ssh_key.pub $SSH_HOME/.ssh/authorized_keys

# Set correct, restrictive permissions on the public key file
RUN chmod 700 $SSH_HOME/.ssh && \
    chmod 600 $SSH_HOME/.ssh/authorized_keys && \
    chown $SSH_USER:$SSH_USER $SSH_HOME/.ssh/authorized_keys

# 3. Configure sshd to only allow key-based login
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config && \
    echo "AllowUsers $SSH_USER" >> /etc/ssh/sshd_config

# Setup application directory (optional, but good practice)
RUN mkdir -p /app/scripts
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

RUN echo '#!/usr/bin/env python3\nimport sys\nprint(f"Hello from Python: {sys.argv[1]}")' > /app/scripts/test.py
RUN chmod +x /app/scripts/test.py
RUN chown -R $SSH_USER:$SSH_USER /app

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]