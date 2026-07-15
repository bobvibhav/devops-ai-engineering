"""Mini Exercise
Write a function called check_servers(server_list) that takes a list of dictionaries — each with 
'name' and 'cpu' keys — and prints a warning for any server above 80% CPU.
Example input: [{'name': 'api-1', 'cpu': 45}, {'name': 'api-2', 'cpu': 91}]
Expected output: WARNING: api-2 at 91% CPU
"""

def check_servers(server_list):
        for server in server_list:
                if server["cpu"] > 80:
                        print (f"WARNING: {server['name']} at {server['cpu']}% CPU")
                

server_list = [{'name': 'api-1', 'cpu': 45}, {'name': 'api-2', 'cpu': 91}]
check_servers(server_list)