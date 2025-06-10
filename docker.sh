#!/bin/bash

# kanjiconv MCP Server Docker Helper Scripts

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to build the Docker image
build() {
    print_status "Building kanjiconv MCP server Docker image..."
    check_docker
    
    # Try building with main Dockerfile first
    if ! docker build -t kanjiconv-mcp:latest .; then
        print_warning "Main Dockerfile failed, trying alternative Dockerfile with pip..."
        if docker build -f Dockerfile.pip -t kanjiconv-mcp:latest .; then
            print_success "Docker image built successfully with pip!"
        else
            print_error "Failed to build Docker image with both methods."
            exit 1
        fi
    else
        print_success "Docker image built successfully with uv!"
    fi
}

# Function to build with specific dockerfile
build-pip() {
    print_status "Building kanjiconv MCP server Docker image with pip..."
    check_docker
    
    docker build -f Dockerfile.pip -t kanjiconv-mcp:latest .
    
    if [ $? -eq 0 ]; then
        print_success "Docker image built successfully with pip!"
    else
        print_error "Failed to build Docker image with pip."
        exit 1
    fi
}

# Function to run the container with docker-compose
up() {
    print_status "Starting kanjiconv MCP server with docker-compose..."
    check_docker
    
    docker-compose up -d
    
    if [ $? -eq 0 ]; then
        print_success "kanjiconv MCP server started successfully!"
        print_status "Use 'docker-compose logs -f' to view logs"
        print_status "Use './docker.sh down' to stop the server"
    else
        print_error "Failed to start the server."
        exit 1
    fi
}

# Function to stop the container
down() {
    print_status "Stopping kanjiconv MCP server..."
    check_docker
    
    docker-compose down
    
    if [ $? -eq 0 ]; then
        print_success "kanjiconv MCP server stopped successfully!"
    else
        print_error "Failed to stop the server."
        exit 1
    fi
}

# Function to view logs
logs() {
    print_status "Showing kanjiconv MCP server logs..."
    check_docker
    
    docker-compose logs -f
}

# Function to restart the service
restart() {
    print_status "Restarting kanjiconv MCP server..."
    down
    up
}

# Function to run the container interactively for testing
test() {
    print_status "Running kanjiconv MCP server in test mode..."
    check_docker
    
    docker run --rm -it kanjiconv-mcp:latest
}

# Function to open a shell in the container
shell() {
    print_status "Opening shell in kanjiconv MCP server container..."
    check_docker
    
    docker-compose exec kanjiconv-mcp /bin/bash
}

# Function to clean up Docker resources
clean() {
    print_warning "This will remove the Docker image and volumes. Are you sure? (y/N)"
    read -r response
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        print_status "Cleaning up Docker resources..."
        
        # Stop and remove containers
        docker-compose down -v
        
        # Remove the image
        docker rmi kanjiconv-mcp:latest 2>/dev/null || true
        
        # Remove unused volumes
        docker volume prune -f
        
        print_success "Cleanup completed!"
    else
        print_status "Cleanup cancelled."
    fi
}

# Function to show help
help() {
    echo "kanjiconv MCP Server Docker Helper"
    echo ""
    echo "Usage: $0 {build|build-pip|up|down|logs|restart|test|shell|clean|help}"
    echo ""
    echo "Commands:"
    echo "  build      - Build the Docker image (tries uv first, fallback to pip)"
    echo "  build-pip  - Build the Docker image using pip explicitly"
    echo "  up         - Start the server with docker-compose"
    echo "  down       - Stop the server"
    echo "  logs       - View server logs"
    echo "  restart    - Restart the server"
    echo "  test       - Run the server in test mode (interactive)"
    echo "  shell      - Open a shell in the running container"
    echo "  clean      - Remove Docker image and volumes"
    echo "  help       - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 build         # Build the image (auto-select method)"
    echo "  $0 build-pip     # Build with pip explicitly"
    echo "  $0 up            # Start the server"
    echo "  $0 logs          # View logs"
    echo "  $0 down          # Stop the server"
}

# Main script logic
case "${1:-help}" in
    build)
        build
        ;;
    up)
        up
        ;;
    down)
        down
        ;;
    logs)
        logs
        ;;
    restart)
        restart
        ;;
    test)
        test
        ;;
    shell)
        shell
        ;;
    clean)
        clean
        ;;
    help|--help|-h)
        help
        ;;
    *)
        print_error "Unknown command: $1"
        help
        exit 1
        ;;
esac
