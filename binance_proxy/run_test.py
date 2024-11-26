import subprocess
import time
import pexpect
import socket

def check_tunnel():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 8080))
        sock.close()
        return result == 0
    except:
        return False

def create_tunnel():
    try:
        print("Starting SSH tunnel with SOCKS proxy...")
        # Using SOCKS proxy tunnel instead
        cmd = 'ssh -D 8080 -C -N -v root@138.197.180.191'
        child = pexpect.spawn(cmd, encoding='utf-8')
        
        i = child.expect(['password:', pexpect.EOF], timeout=30)
        if i == 0:
            child.sendline('jEtsrus33J')
            print("Password sent, waiting for tunnel...")
            time.sleep(5)
            
            if check_tunnel():
                print("SOCKS proxy is listening!")
                return child
            else:
                print("Port 8080 is not listening. Tunnel may have failed.")
                return None
    except Exception as e:
        print(f"Tunnel error: {e}")
        return None

def test_binance_connection():
    import requests
    from urllib3.contrib.socks import SOCKSProxyManager
    
    print("\nTesting connection through SOCKS proxy...")
    proxy_url = "socks5h://127.0.0.1:8080"
    
    try:
        # Use SOCKSProxyManager instead of regular requests
        proxy = SOCKSProxyManager(proxy_url)
        response = proxy.request(
            'GET',
            'https://api.binance.com/api/v3/time',
            timeout=10.0
        )
        print(f"Response: {response.data.decode()}")
        return True
    except Exception as e:
        print(f"Connection error: {str(e)}")
        return False

def main():
    # Kill any existing tunnels
    subprocess.run(['pkill', '-f', 'ssh -D 8080'])
    time.sleep(2)
    
    print("\nSetting up SOCKS tunnel...")
    tunnel = create_tunnel()
    
    if tunnel:
        try:
            # Try multiple times with delay
            for i in range(3):
                print(f"\nAttempt {i+1}...")
                if test_binance_connection():
                    break
                time.sleep(3)
            
            print("\nPress CTRL+C to stop tunnel")
            while True:
                if not check_tunnel():
                    print("Tunnel appears to be down!")
                    break
                time.sleep(1)
                
        except KeyboardInterrupt:
            pass
        finally:
            print("\nClosing tunnel...")
            tunnel.close()
            subprocess.run(['pkill', '-f', 'ssh -D 8080'])
    else:
        print("Failed to create tunnel")

if __name__ == "__main__":
    main()
