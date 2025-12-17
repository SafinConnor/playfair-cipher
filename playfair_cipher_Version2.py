def generate_playfair_table(key):
    key = key.upper().replace('J', 'I')
    key = ''.join([c for c in key if c.isalpha()])
    
    seen = set()
    unique_chars = []
    for char in key:
        if char not in seen:
            unique_chars.append(char)
            seen.add(char)
    
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    for char in alphabet:
        if char not in seen:
            unique_chars.append(char)
            seen.add(char)
    
    table = []
    for i in range(5):
        row = unique_chars[i*5:(i+1)*5]
        table.append(row)
    
    return table


def preprocess_message(message):
    message = message.upper().replace('J', 'I')
    message = ''.join([c for c in message if c.isalpha()])
    
    digraphs = []
    i = 0
    
    while i < len(message):
        char1 = message[i]
        
        if i + 1 < len(message):
            char2 = message[i + 1]
            
            if char1 == char2:
                if char1 == 'X':
                    digraphs.append(char1 + 'Z')
                else:
                    digraphs.append(char1 + 'X')
                i += 1
            else:
                digraphs.append(char1 + char2)
                i += 2
        else:
            if char1 == 'X':
                digraphs.append('XZ')
            else:
                digraphs.append(char1 + 'X')
            i += 1
    
    return digraphs


def find_position(char, table):
    for row in range(5):
        for col in range(5):
            if table[row][col] == char:
                return (row, col)
    return None


def encrypt_digraph(digraph, table):
    char1, char2 = digraph[0], digraph[1]
    row1, col1 = find_position(char1, table)
    row2, col2 = find_position(char2, table)
    
    if row1 == row2:
        new_col1 = (col1 + 1) % 5
        new_col2 = (col2 + 1) % 5
        return table[row1][new_col1] + table[row2][new_col2]
    elif col1 == col2:
        new_row1 = (row1 + 1) % 5
        new_row2 = (row2 + 1) % 5
        return table[new_row1][col1] + table[new_row2][col2]
    else:
        return table[row1][col2] + table[row2][col1]


def decrypt_digraph(digraph, table):
    char1, char2 = digraph[0], digraph[1]
    row1, col1 = find_position(char1, table)
    row2, col2 = find_position(char2, table)
    
    if row1 == row2:
        new_col1 = (col1 - 1) % 5
        new_col2 = (col2 - 1) % 5
        return table[row1][new_col1] + table[row2][new_col2]
    elif col1 == col2:
        new_row1 = (row1 - 1) % 5
        new_row2 = (row2 - 1) % 5
        return table[new_row1][col1] + table[new_row2][col2]
    else:
        return table[row1][col2] + table[row2][col1]


def encrypt(plaintext, key):
    table = generate_playfair_table(key)
    digraphs = preprocess_message(plaintext)
    
    ciphertext = ''
    for digraph in digraphs:
        ciphertext += encrypt_digraph(digraph, table)
    
    return ciphertext, table, digraphs


def decrypt(ciphertext, key):
    table = generate_playfair_table(key)
    
    ciphertext = ciphertext.upper().replace('J', 'I')
    ciphertext = ''.join([c for c in ciphertext if c.isalpha()])
    digraphs = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]
    
    plaintext = ''
    for digraph in digraphs:
        plaintext += decrypt_digraph(digraph, table)
    
    return plaintext, table, digraphs


def display_table(table):
    print("\n" + "="*21)
    print("   PLAYFAIR TABLE")
    print("="*21)
    for row in table:
        print("  " + ' '.join(row))
    print("="*21)


def display_digraphs(digraphs):
    print("\nDigraphs:  " + ' | '.join(digraphs))


def run_tests():
    print("\n" + "#"*60)
    print("# RUNNING MANDATORY TEST CASES")
    print("#"*60)
    
    all_passed = True
    
    # Test 1: Standard message
    print("\n" + "─"*60)
    print("TEST 1: Standard Message")
    print("─"*60)
    key1 = "PLAYFAIR"
    plain1 = "HIDETHEGOLDINTHETREESTUMP"
    expected1 = "EBIMQMGHVRIRONKGODKUKNNZEF"
    
    result1, table1, digraphs1 = encrypt(plain1, key1)
    
    print(f"Key:        {key1}")
    print(f"Plaintext: {plain1}")
    display_table(table1)
    display_digraphs(digraphs1)
    print(f"\nExpected:  {expected1}")
    print(f"Got:       {result1}")
    
    test1_pass = result1 == expected1
    print(f"\n{'✓ PASS' if test1_pass else '✗ FAIL'}")
    all_passed = all_passed and test1_pass
    
    # Test 2: Message ending in X with odd length
    print("\n" + "─"*60)
    print("TEST 2: Message Ending in X (ABX)")
    print("─"*60)
    message2 = "ABX"
    _, _, digraphs2 = encrypt(message2, "TEST")
    
    print(f"Message:   {message2}")
    display_digraphs(digraphs2)
    print(f"Expected:   AB | XZ")
    
    test2_pass = digraphs2 == ['AB', 'XZ']
    print(f"\n{'✓ PASS' if test2_pass else '✗ FAIL'}")
    all_passed = all_passed and test2_pass
    
    # Test 3: Single character X
    print("\n" + "─"*60)
    print("TEST 3: Single Character X")
    print("─"*60)
    message3 = "X"
    _, _, digraphs3 = encrypt(message3, "TEST")
    
    print(f"Message:   {message3}")
    display_digraphs(digraphs3)
    print(f"Expected:  XZ")
    
    test3_pass = digraphs3 == ['XZ']
    print(f"\n{'✓ PASS' if test3_pass else '✗ FAIL'}")
    all_passed = all_passed and test3_pass
    
    # Test 4: Message with double letters (HELLO)
    print("\n" + "─"*60)
    print("TEST 4: Message with Double Letters (HELLO)")
    print("─"*60)
    message4 = "HELLO"
    _, _, digraphs4 = encrypt(message4, "TEST")
    
    print(f"Message:   {message4}")
    display_digraphs(digraphs4)
    print(f"Expected:  HE | LX | LO")
    
    test4_pass = digraphs4 == ['HE', 'LX', 'LO']
    print(f"\n{'✓ PASS' if test4_pass else '✗ FAIL'}")
    all_passed = all_passed and test4_pass
    
    # Test 5: Complete ARLATHAN example
    print("\n" + "─"*60)
    print("TEST 5: Complete ARLATHAN Example")
    print("─"*60)
    key5 = "ARLATHAN"
    plain5 = "GARDIENIIVORDESCHIDEPOARTALAMIEZULNOPTIXIX"
    expected5 = "FRTBMCCFFXPAENQDLMENQPRLHRTRFKMHQHFVSRQLQL"
    
    result5, table5, digraphs5 = encrypt(plain5, key5)
    
    print(f"Key:       {key5}")
    print(f"Plaintext: {plain5}")
    display_table(table5)
    display_digraphs(digraphs5)
    print(f"\nExpected:  {expected5}")
    print(f"Got:       {result5}")
    
    test5_pass = result5 == expected5
    print(f"\n{'✓ PASS' if test5_pass else '✗ FAIL'}")
    all_passed = all_passed and test5_pass
    
    # Test 6: Decryption verification
    print("\n" + "─"*60)
    print("TEST 6: Decryption Test (ARLATHAN)")
    print("─"*60)
    decrypted, _, dec_digraphs = decrypt(result5, key5)
    
    print(f"Ciphertext: {result5}")
    display_digraphs(dec_digraphs)
    print(f"Decrypted:  {decrypted}")
    print(f"Original:   {plain5}")
    
    test6_pass = decrypted == plain5
    print(f"\n{'✓ PASS' if test6_pass else '✗ FAIL'}")
    all_passed = all_passed and test6_pass
    
    # Summary
    print("\n" + "#"*60)
    if all_passed:
        print("# ✓ ALL TESTS PASSED!")
    else:
        print("# ✗ SOME TESTS FAILED")
    print("#"*60 + "\n")


def main():
    print("\n" + "="*60)
    print("          PLAYFAIR CIPHER - ENCRYPTION & DECRYPTION")
    print("="*60)
    
    while True:
        print("\n" + "─"*60)
        print("OPTIONS:")
        print("  [1] Encrypt a message")
        print("  [2] Decrypt a message")
        print("  [3] Run mandatory test cases")
        print("  [4] Exit")
        print("─"*60)
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            # Encryption mode
            print("\n" + "─"*60)
            print("ENCRYPTION MODE")
            print("─"*60)
            
            key = input("Enter the key:  ").strip()
            plaintext = input("Enter the plaintext: ").strip()
            
            if not key or not plaintext:
                print("\n⚠ Error: Key and plaintext cannot be empty!")
                continue
            
            ciphertext, table, digraphs = encrypt(plaintext, key)
            
            display_table(table)
            print(f"\nOriginal message:  {plaintext}")
            print(f"Preprocessed:      {''.join(digraphs)}")
            display_digraphs(digraphs)
            print(f"\n🔒 CIPHERTEXT: {ciphertext}")
            
        elif choice == '2':
            # Decryption mode
            print("\n" + "─"*60)
            print("DECRYPTION MODE")
            print("─"*60)
            
            key = input("Enter the key: ").strip()
            ciphertext = input("Enter the ciphertext: ").strip()
            
            if not key or not ciphertext:
                print("\n⚠ Error: Key and ciphertext cannot be empty!")
                continue
            
            plaintext, table, digraphs = decrypt(ciphertext, key)
            
            display_table(table)
            print(f"\nCiphertext:  {ciphertext}")
            display_digraphs(digraphs)
            print(f"\n🔓 PLAINTEXT: {plaintext}")
            
        elif choice == '3':
            # Run tests
            run_tests()
            
        elif choice == '4':
            # Exit
            print("\n👋 Thank you for using Playfair Cipher!")
            print("="*60 + "\n")
            break
            
        else:
            print("\n⚠ Invalid choice! Please enter 1, 2, 3, or 4.")


if __name__ == "__main__": 
    main()