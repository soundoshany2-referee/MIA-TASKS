"""
Task 1.2: Stadium Gate Ticket Codec
--------------------------------------
A TicketCodec that embeds a simple checksum into a barcode, so a gate
scanner can instantly tell if a ticket ID was tampered with.
"""


class TicketCodec:

    def _compute_checksum(self, ticket_id):
        """
        How this checksum works:
        We go through every character in the ticket_id and add up
        (character code * its position number). Multiplying by position
        means that even swapping two characters (not just changing one)
        will usually change the result, not just changing a single letter.
        Finally we take the result modulo 97 so it stays a small 2-digit
        number, and format it with a leading zero if needed (e.g. "05").
        """
        total = 0
        for index, char in enumerate(ticket_id):
            total += ord(char) * (index + 1)
        return total % 97

    def encode(self, ticket_id):
        """Takes a ticket ID and returns 'TICKETID-CHECKSUM'."""
        checksum = self._compute_checksum(ticket_id)
        return f"{ticket_id}-{checksum:02d}"

    def decode(self, barcode):
        """
        Splits the barcode back into ticket_id and checksum, recomputes
        the checksum from the ticket_id, and compares. If they match,
        the ticket is valid. If not (or the format looks wrong), it's
        flagged as corrupted.
        """
        if "-" not in barcode:
            return "CORRUPTED TICKET"

        ticket_id, _, checksum_text = barcode.rpartition("-")

        if not checksum_text.isdigit():
            return "CORRUPTED TICKET"

        expected_checksum = self._compute_checksum(ticket_id)

        if int(checksum_text) == expected_checksum:
            return ticket_id
        else:
            return "CORRUPTED TICKET"


if __name__ == "__main__":
    codec = TicketCodec()

    # 1) Encode a few sample ticket IDs
    sample_ids = ["MIA2026GATE7", "VIP001SECTIONA", "STDNT4587"]
    barcodes = []

    print("--- Encoding sample tickets ---")
    for ticket_id in sample_ids:
        barcode = codec.encode(ticket_id)
        barcodes.append(barcode)
        print(f"encode({ticket_id!r}) -> {barcode!r}")

    # 2) Decode each barcode as-is (should all succeed)
    print("\n--- Decoding untouched barcodes ---")
    for barcode in barcodes:
        result = codec.decode(barcode)
        print(f"decode({barcode!r}) -> {result!r}")

    # 3) Hand-corrupt one character in the first barcode's ticket portion
    print("\n--- Decoding a tampered barcode ---")
    original_barcode = barcodes[0]
    ticket_part, _, checksum_part = original_barcode.rpartition("-")

    # Flip the last character of the ticket ID to something different
    last_char = ticket_part[-1]
    new_char = "9" if last_char != "9" else "8"
    corrupted_ticket = ticket_part[:-1] + new_char
    corrupted_barcode = f"{corrupted_ticket}-{checksum_part}"

    print(f"Original barcode:  {original_barcode!r}")
    print(f"Corrupted barcode: {corrupted_barcode!r}")
    print(f"decode({corrupted_barcode!r}) -> {codec.decode(corrupted_barcode)!r}")
