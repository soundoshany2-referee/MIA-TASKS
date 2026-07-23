class TicketCodec:

    def calculate_checksum(self, ticket_id):
        total = 0

        for i in range(len(ticket_id)):
            total += ord(ticket_id[i]) * (i + 1)

        checksum = total % 100

        if checksum < 10:
            return "0" + str(checksum)
        else:
            return str(checksum)

    def encode(self, ticket_id):
        checksum = self.calculate_checksum(ticket_id)
        return ticket_id + "-" + checksum

    def decode(self, barcode):

        parts = barcode.split("-")

        if len(parts) != 2:
            return "CORRUPTED TICKET"

        ticket_id = parts[0]
        saved_checksum = parts[1]

        new_checksum = self.calculate_checksum(ticket_id)

        if saved_checksum == new_checksum:
            return ticket_id
        else:
            return "CORRUPTED TICKET"


codec = TicketCodec()

ticket1 = "MIA2026GATE7"
ticket2 = "FINAL123"
ticket3 = "ABC987"

barcode1 = codec.encode(ticket1)
barcode2 = codec.encode(ticket2)
barcode3 = codec.encode(ticket3)

print("Encoded Tickets:")
print(barcode1)
print(barcode2)
print(barcode3)

print()
print("Decoded Tickets:")
print(codec.decode(barcode1))
print(codec.decode(barcode2))
print(codec.decode(barcode3))

print()
print("Corrupted Ticket Test:")

bad_barcode = "MIA2026GATE8-35"

print(bad_barcode)
print(codec.decode(bad_barcode))