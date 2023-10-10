from itertools import combinations
import ast

def reverse_engineering_packet(packet):
    max_bytes_per_part = 1  # Define maximum bytes per part
    packet_length = len(packet)
    all_possible_breaks = []

    # Generate all possible breaks in the packet
    for r in range(1, packet_length):
        all_possible_breaks.extend(combinations(range(1, packet_length), r))
    
    # Loop through each possible partitioning of the packet
    for possible_break in all_possible_breaks:
        prev = 0
        valid_break = True
        parsed_data = []
        
        # Check each segment to make sure it doesn't exceed max_bytes_per_part
        for brk in possible_break:
            if brk - prev > max_bytes_per_part:
                valid_break = False
                break
            segment = packet[prev:brk]
            parsed_data.append(segment)
            prev = brk
        
        # Add the last segment
        segment = packet[prev:]
        if len(segment) > max_bytes_per_part:
            valid_break = False
        else:
            parsed_data.append(segment)

        if valid_break:
            # Output the parsed data as integers, for example
            parsed_as_ints = [int.from_bytes(seg, 'big') for seg in parsed_data]
            print("Possible partition:", parsed_as_ints)

# Example usage
if __name__ == "__main__":
    with open("packets.txt", "r") as f:
        for line in f:
            # Convert the string back to its byte representation
            packet_as_bytes = bytes(ast.literal_eval("b'" + line.strip() + "'"))
            reverse_engineering_packet(packet_as_bytes)