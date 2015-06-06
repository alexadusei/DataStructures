"""
    Purpose: To test the length of hash tables using two types of addressing:
             Quadratic Probing and Double Hashing. These tests determine the
             best (smallest) table size given the requirements (average
             comparison <= 4).
"""
#-------------------------------------------------------------------------------

import math

def main():
    """ tableSizes is an list of 200 primes from 2003 onwards. The reason
        this list exists is because through experimentation, prime values of
        m generally produce better probing than ordinary
    """

    global comparisons
    agentList = read_names()
    tableSizes = primes(200)
    c = [(1, 1), (1.5, 1.5), (11, 13)] # constants
    hashFns = [elf_hash, sdbm_hash, djb2_hash]

    # simple naming scheme. A key-value sort of mechanism is in place, where the
    # first two characters are using in our open_address function to give the
    # queryType, and the remaining characters are to be displayed
    openAddressTypes = ["qp-QUADRATIC PROBING", "dh-DOUBLE HASHING"]
    hashNames= ["ELF Hash", "SDBM Hash", "DJB2 Hash"]

    # The run down of these for loops is that, starting at a tableSize of 2003
    # it will begin open addressing and keeping track of comparisons. If the
    # average comparison is greater than 4, that iteration is discared. Also if
    # the table returns 'F' for Full, the iteration is also discarded. This
    # continues for increasing indexes of prime sizes in tableSizes. Once the
    # process passes the criteria, the current table is used, and that is the
    # best, and smallest table possible.
    for oaType in openAddressTypes:
        print "-----", oaType[3:], "-----\n"

        filledSpots = 0

        if oaType[:2] == "qp": print "h(k):", hashNames[1], "\n"

        for i in range(len(c)):

            h1 = hashFns[i] if oaType[:2] == "dh" else hashFns[1]
            h2 = hashFns[-len(hashFns)] if (i+1) == len(hashFns) else hashFns[i+1]

            hashName1 = hashNames[i] if oaType[:2] == "dh" else hashNames[0]
            hashName2 = hashNames[-len(hashFns)] if (i+1) == len(hashFns) \
                    else hashNames[i+1]

            if oaType[:2] == "dh":
                print "h'(k):", hashName1
                print "h\"(k):", hashName2, "\n"

            if oaType[:2] == "qp":
                print "c1 =", str(c[i][0])
                print "c2 =", c[i][1]

            for tableSize in tableSizes:
                hashTable = create_table(tableSize)
                comparisons = 0
                result = 'NF'

                for agent in agentList:
                    if result == 'F':
                        break
                    result = open_address(agent, hashTable, c[i][0] , c[i][1],\
                                h1, h2, "i", oaType[:2])

                # This if statement finds the first table size that has an avg
                # less than or equal to 4, and prints that as the result
                if result == 'NF':
                    filledSpots = len([x for x in hashTable if x != ''])
                    if round(float(comparisons) / filledSpots, 2) <= 4:
                        break

            isZero = 1 if filledSpots == 0 else 0 # prevents dividing by zero

            print "Smallest table size:\t", len(hashTable)
            print "Total comparisons:" + "\t"*2, comparisons
            print "Avg comparisons:" + "\t"*2, round(float(comparisons) /
                (filledSpots+isZero), 2), "\n"

#-----------------------------Auxiliary Functions-------------------------------

# Returns an array of all text-names
def read_names():
    return [line.strip() for line in open("top_secret_agent_aliases_2015.txt", "r")]

# Returns an array (a hash table in this case) of empty addresses ("")
def create_table(size):
    return ["" for i in range(size)]

def primes(numOfPrimes):
    """ Auxiliary function that finds and returns a list of n primes, where n
        is the number of primes."""

    primes = []
    # we want to start at 2003, which is the first prime after 2000, seeing as
    # we absolutely need to fit all 2000 keys on the hash table,
    i = 2003

    while len(primes) < numOfPrimes:
        isPrime = True

        for k in range(2, i):
            if i % k == 0:
                isPrime = False
                break

        if isPrime:
            primes.append(i)
        i += 1

    return primes

def isPrime(number):
    if number < 2:
        return False

    for i in range(2, number):
        if number % i == 0:
            return False
    return True

#-----------------------------HASH FUNCTIONS------------------------------------

def djb2_hash(key):
    """ Bernstein Hash by Professor Dan J. Bernstein. He created an original
        called the DJB hash, and it was modified for better distribution, named
        DJB2. It performs very well in practice, for no apparently known reasons
        (much like how the constant 5381 does better than more logical constants
        for no apparent reason). """

    hash = 5381

    for i in range(len(key)):
        hash = ((hash << 5) + hash) + ord(key[i])

    return hash

def sdbm_hash(key):
    """ This is the algorithm of choice which was used in the open source SDBM
        project. The hash function seems to have a good over-all distribution
        for many different data sets. It seems to work well in situations where
        there is a high variance in the most sigificant bits s of the
        elements in a data set. """

    hash = 0

    for i in range(len(key)):
        hash = ord(key[i]) + (hash << 6) + (hash << 16) - hash

    return (hash & 0x7FFFFFFF)

def elf_hash(key):
    """ ELF Hash is another popular choice among good-performining string hash
        functions """

    hash = 0
    x = 0

    for i in range(len(key)):
        hash = (hash << 4) + ord(key[i])
        x = hash & 0xF0000000

        if x != 0:
            hash **= (x >24)

        hash &= ~x

    return (hash & 0x7FFFFFFF)

#--------------------------------Open Addressing--------------------------------

def open_address(key, table, c1, c2, hk1, hk2, queryType="i", OAType="qp"):
    """ The function for handling all opening addressing for both quadratic
        probing and double hashing, whether it is an insertion or a search.

        Parameters: key, hash table, constant#1, constant#2, hash function#1,
                    hash function#2, query type ('i' for insertion, elsewise
                    for a search), and open-address type ('qp' for quadratic
                    probing, elsewise for double hashing)

        The function simply uses conditional statements and if-statements to
        make a decision based on what queryType and OAType are. Because
        queryType and OAType have default values, we can leave them blank when
        calling the functions. The functions uses 's' to denote 'search' and
        'dh' to denote 'double hashing'. """

    global comparisons
    i = 0
    m = len(table)
    comparisons += 1 # we ++ comparisons here just for initiating an insert

    value1 = hk1(key)
    value2 = hk2(key) if OAType == "dh" else 0
    address = (value1 + (i+1)*value2) % m

    while i < len(table) and table[address] != '':
        if queryType == "s" and table[address] == key:
            break

        i += 1
        comparisons += 1

        address = int(math.ceil(value1+(i+1)*(value2+1)))%m if OAType == "dh"\
            else int(math.ceil(value1 + c1*i + c2*i**2)) % m

    if queryType == "s" and table[address] == key:
        print "Found", key
    elif queryType != "s" and table[address] == '':
        table[address] = key
        return 'NF' # Table 'Not Full'
    else:
        if queryType == "s": print "Search failed"; return
        return 'F' # Table 'Full'

comparisons = 0
main()
