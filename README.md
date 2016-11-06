## Master Password Generator

Generate a master password that is a random combination of words, fake words, symbols and of a minimum length.

## Motivation

After watching these Computerphile [Password Cracking](https://www.youtube.com/watch?v=7U-RbOKanYs) and [Password Choice](https://www.youtube.com/watch?v=3NjQ9b3pgIg) videos, I decided to code up a simple master password generator.

## Code Example

Below shows the usage and example passwords generated using ```master_password_generator.py```:

```
▶ python master_password_generator.py -h
usage: master_password_generator.py [-h] [--obscurity {0.1-1.0}]
                                    [--user_words USER_WORDS]
                                    [--word_override] [--symbols SYMBOLS]
                                    [--caps CAPS]
                                    {10-50}

Generate master passwords for password managers. This code uses a random
sample of the top 1/3M words along with user words and symbols. It generates
long un-brute-force-able passwords that should be resilient to dictionary
cracks also.

positional arguments:
  {10-50}               Minimum number of characters in password

optional arguments:
  -h, --help            show this help message and exit
  --obscurity {0.1-1.0}
                        Level of obscurity for password words. Smaller number
                        means more obscure.
  --user_words USER_WORDS
                        Comma separated list of user words to include
  --word_override       Override check for user words duplicated in the real
                        word list
  --symbols SYMBOLS     Number of random symbols to insert in final password
  --caps CAPS           Number of characters to convert to upper case in final
                        password
```

To make a password with 30 characters using the 50% most obscure words from [Peter Norvig's 1/3 million most commonly used English words], with 2 randomly inserted symbols, 2 random letter capitalisations and 2 fake words, we use:

```
▶ python master_password_generator.py 30 --obscurity 0.5 --symbols 2 --caps 2 --fake_words xkcd,hipnox
```

This returns:

```
Password word list: ['xkcd', 'hipnox', 'pronostic', 'pilotless', 'seaduw']
Password shuffled string: hipnoxpronosticxkcdseaduwpilotless
Capitalising character indices: [31, 16]
hipnoxpronosticxKcdseaduwpilotlEss
Adding random symbols at indices: [9, 22]
MASTER PASSWORD: hipnoxpro>nosticxKcdse;aduwpilotlEss
0:00:00.489549
```

The locations of the symbols and letter capitalisation are chosen at random. This example password would take 4 quindecillion years to brute force. The random combination of random and user supplied (possibly made up) words, with a few random symbols and capitalizations makes it robust to dictionary cracking too.

To generate a password with all your own words you can supply all words manually using the ```--user_words``` option. No random words will be incorporated, so long as their combined length is longer than the minimum length supplied on the command line.

```
▶ python  master_password_generator.py 12 --obscurity 1.0 --symbols 2 --user_words horse,plough,wobble,friction --word_override --caps 2
```

This returns:

```
Password word list: ['horse', 'plough', 'wobble', 'friction']
Password shuffled string: ploughhorsefrictionwobble
Capitalising character indices: [5, 1]
pLougHhorsefrictionwobble
Adding random symbols at indices: [8, 15]
MASTER PASSWORD: pLougHho+rsefri@ctionwobble
0:00:00.488626
```

This password would take 1 undecillion years to brute force crack.

## Installation

```
git clone https://github.com/jmccormac01/MasterPasswordGenerator.git
```

## API Reference

N/A

## Tests

Add a password cracking test to check the outputs

## Contributors

James McCormac

## License

MIT
