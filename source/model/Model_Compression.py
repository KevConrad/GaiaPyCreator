import bitstring

class Model_Compression:

    # Quintet Decompressor
    # Written by Alchemic
    # 2011 Jul 19
    # 
    # 
    # 
    # This compression format is used by five of Quintet's games:
    #   - ActRaiser
    #   - ActRaiser 2
    #   - Illusion of Gaia
    #   - Robotrek
    #   - Soul Blazer
    # 
    # A terse description of the compression format:
    # 
    #    LZSS with a 256-byte sliding window and a 16-byte lookahead, 
    #    allowing copying of 2-17 previously-seen bytes. The window 
    #    is initially filled with 0x20s. References to past data use 
    #    absolute positions in the window and decompressed bytes are 
    #    written in the window starting at position 0xEF. Control 
    #    bits (indicating what follows is pastcopy or literal) are
    #    part of the stream, rather than being grouped into eights 
    #    and packed into their own bytes.
    # 
    # 
    # 
    # In greater detail:
    # 
    #   - Compressed data is prefixed with a 16-bit integer indicating 
    #     the length of the data once decompressed.
    # 
    #   - Following this is the compressed data itself: a stream of 
    #     bits that breaks down into two commands, "pastcopy" and 
    #     "literal". Bits are read from one byte at a time, most 
    #     significant to least (0x80, 0x40, 0x20 ... 0x01).
    # 
    #        Pastcopy = [0 SSSSSSSS LLLL]
    #        Literal  = [1 NNNNNNNN]
    # 
    #   - Pastcopy copies data from the sliding window. The S argument
    #     is the source, which is an absolute position in the sliding
    #     window (i.e. NOT relative to the last-written position); the
    #     L argument indicates how many bytes to copy. Since we'd never
    #     copy 0 bytes (wastes 13 bits to do nothing) or 1 byte (using
    #     a literal saves 4 bits), we actually copy L+2 bytes.
    # 
    #   - Literal is exactly what it says on the tin. The N argument 
    #     is one uncompressed byte.
    # 
    #   - Whenever we decompress a byte, we write it to both the output
    #     buffer and the sliding window. Curiously, we don't start at
    #     the beginning of the window. Instead, the first decompressed
    #     byte goes to position 0xEF, the second to position 0xF0, and
    #     so on up, wrapping after 0xFF to 0x00.
    # 
    #   - The sliding window is initially populated with 0x20s. One 
    #     consequence of this is pastcopies from "negative" positions
    #     (i.e. copying from sliding window positions that haven't 
    #     been filled with decompressed bytes yet), which happens if 
    #     the original data had 0x20s early on.
    # 
    # 
    # 
    # This code uses python-bitstring version 2.2.0:
    # http://code.google.com/p/python-bitstring/
    def decompress(romData, dataOffset, dataSize):
        # Define some useful constants.
        SEARCH_LOG2 = 8
        SEARCH_SIZE = 1 << SEARCH_LOG2
        LOOKAHEAD_LOG2 = 4
        LOOKAHEAD_SIZE = 1 << LOOKAHEAD_LOG2
        BIT_PASTCOPY = 0
        BIT_LITERAL = 1
        
        # Open the ROM.
        romStream = bitstring.ConstBitStream(bytes = romData, offset=(dataOffset * 8), length=(dataSize * 8))

        # Allocate memory for the decompression process.
        decompSize = romStream.read('uintle:16')
        decomp = bytearray([0x00] * decompSize)
        decompPos = 0
        window = bytearray([0x20] * SEARCH_SIZE)
        windowPos = 0xEF

        try:
            # Main decompression loop.
            while decompPos < decompSize:
                nextCommand = romStream.read('bool')

                if nextCommand == BIT_PASTCOPY:
                    # 0: Pastcopy case.
                    copySource = romStream.read(SEARCH_LOG2).uint
                    copyLength = romStream.read(LOOKAHEAD_LOG2).uint
                    copyLength += 2

                    # Truncate copies that would exceed "decompSize" bytes.
                    if (decompPos + copyLength) >= decompSize:
                        copyLength = decompSize - decompPos

                    for i in range(copyLength):
                        decomp[decompPos] = window[copySource]
                        decompPos += 1
                        window[windowPos] = window[copySource]
                        windowPos += 1
                        windowPos &= (SEARCH_SIZE - 1)
                        copySource += 1
                        copySource &= (SEARCH_SIZE - 1)

                elif nextCommand == BIT_LITERAL:
                    # 1: Literal case.
                    literalByte = romStream.read('uint:8')
                    decomp[decompPos] = literalByte
                    decompPos += 1
                    window[windowPos] = literalByte
                    windowPos += 1
                    windowPos &= (SEARCH_SIZE - 1)
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)

        # Calculate the end offset.
        romStream.bytealign()
        endOffset = romStream.bytepos

        # Return the decompressed data and end offset.
        return (decomp, endOffset)
    
    # Quintet Compressor
    # Written by Alchemic
    # 2012 Feb 04
    # 
    # 
    # 
    # This compression format is used by five of Quintet's games:
    #   - ActRaiser
    #   - ActRaiser 2
    #   - Illusion of Gaia
    #   - Robotrek
    #   - Soul Blazer
    # 
    # The format is described in greater detail in the decompressor.
    # 
    # 
    # 
    # This code uses python-bitstring version 2.2.0:
    # http://code.google.com/p/python-bitstring/
    def compress(inBytes):
        # Define some useful constants.
        SEARCH_LOG2 = 8
        SEARCH_SIZE = 1 << SEARCH_LOG2
        LOOKAHEAD_LOG2 = 4
        LOOKAHEAD_SIZE = 1 << LOOKAHEAD_LOG2
        BIT_PASTCOPY = 0
        BIT_LITERAL = 1

        # Prepare the memory buffer.
        inBuffer = bytearray(SEARCH_SIZE + len(inBytes))
        inBuffer[:SEARCH_SIZE] = [0x20] * SEARCH_SIZE
        inBuffer[SEARCH_SIZE:] = inBytes

        # Prepare for compression.
        output = bitstring.BitArray()
        output += bitstring.pack('uintle:16', len(inBytes))
        currentIndex = SEARCH_SIZE

        # Main compression loop.
        while currentIndex < len(inBuffer):
            bestIndex = 0
            bestLength = 0

            # Look for a match in the search buffer. (Brute force)
            for i in range(SEARCH_SIZE):
                # Don't compare past the end of the lookahead buffer.
                # Don't compare past the end of the memory buffer.
                compareLimit = min(
                LOOKAHEAD_SIZE - 1,
                len(inBuffer) - currentIndex
                )

                # Compare the search buffer to the lookahead buffer.
                # Count how many sequential bytes match (possibly zero).
                currentLength = 0
                for j in range(compareLimit):
                    if inBuffer[currentIndex - SEARCH_SIZE + i + j] == inBuffer[currentIndex + j]:
                        currentLength += 1
                    else:
                        break

                # Keep track of the largest match we've seen.
                if currentLength > bestLength:
                    bestIndex = currentIndex - SEARCH_SIZE + i
                    bestLength = currentLength

            # Write the next block of compressed output.
            if bestLength >= 2:
                # For some reason, the decompressor expects the pastcopy 
                # source values to be offset by 0xEF. I have no idea why.
                bestIndex = (bestIndex + 0xEF) & 0xFF
                output += bitstring.pack('bool', BIT_PASTCOPY)
                output += bitstring.pack('uint:n=v', n = SEARCH_LOG2, v = bestIndex)
                output += bitstring.pack('uint:n=v', n = LOOKAHEAD_LOG2, v = bestLength - 2)
                currentIndex += bestLength
            else:
                output += bitstring.pack('bool', BIT_LITERAL)
                output += bitstring.pack('uint:8', inBuffer[currentIndex])
                currentIndex += 1

        # Return the compressed data.
        return output.tobytes()
        