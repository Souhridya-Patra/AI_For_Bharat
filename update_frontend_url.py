"""Update frontend API URL for EC2 deployment."""
import sys
from pathlib import Path

def update_frontend_url(ec2_ip):
    """Update the API URL in frontend/index.html."""
    frontend_file = Path("frontend/index.html")
    
    if not frontend_file.exists():
        print("✗ Error: frontend/index.html not found")
        return False
    
    # Read file
    content = frontend_file.read_text(encoding='utf-8')
    
    # Replace localhost with EC2 IP
    content = content.replace(
        "const API_URL = 'http://localhost:8000/v1';",
        f"const API_URL = 'http://{ec2_ip}:8000/v1';"
    )
    
    content = content.replace(
        "const response = await fetch('http://localhost:8000/health');",
        f"const response = await fetch('http://{ec2_ip}:8000/health');"
    )
    
    content = content.replace(
        '<p><a href="http://localhost:8000/docs" target="_blank">API Documentation</a></p>',
        f'<p><a href="http://{ec2_ip}:8000/docs" target="_blank">API Documentation</a></p>'
    )
    
    # Write back
    frontend_file.write_text(content, encoding='utf-8')
    
    print(f"✓ Updated frontend API URL to: http://{ec2_ip}:8000")
    return True

def main():
    """Main function."""
    print("=" * 60)
    print("Update Frontend API URL for EC2 Deployment")
    print("=" * 60)
    print()
    
    if len(sys.argv) < 2:
        print("Usage: python update_frontend_url.py <EC2_PUBLIC_IP>")
        print()
        print("Example:")
        print("  python update_frontend_url.py 54.123.45.67")
        print()
        return
    
    ec2_ip = sys.argv[1]
    
    print(f"EC2 Public IP: {ec2_ip}")
    print()
    
    if update_frontend_url(ec2_ip):
        print()
        print("✓ Frontend updated successfully!")
        print()
        print("Next steps:")
        print("1. Commit and push changes to GitHub")
        print("2. Pull changes on EC2: git pull")
        print("3. Restart frontend: screen -X -S frontend quit && screen -S frontend")
        print()
    else:
        print()
        print("✗ Failed to update frontend")
        print()

if __name__ == "__main__":
    main()
