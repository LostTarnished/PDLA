import pytest
import math
from lark.exceptions import LarkError

from arithmp.parser import Parser

@pytest.fixture(scope="module")
def parser():
    """
    Fixture Pytest : instancie le parseur une seule fois pour tous les tests.
    Cela évite de recharger le fichier .lark à chaque test.
    """
    return Parser()

def test_operations_basiques(parser):
    # Addition et Soustraction
    assert parser.parse("2 + 3") == 5.0
    assert parser.parse("10 - 4") == 6.0
    
    # Multiplication et Division
    assert parser.parse("3 * 4") == 12.0
    assert parser.parse("15 / 3") == 5.0
    
    # Modulo
    assert parser.parse("10 % 3") == 1.0

def test_nombres_decimaux(parser):
    assert parser.parse("2.5 + 2.5") == 5.0
    assert parser.parse("1.5 * 2") == 3.0

def test_operations_unaires(parser):
    assert parser.parse("-5") == -5.0
    assert parser.parse("+5") == 5.0
    assert parser.parse("---5") == -5.0  # Si ta grammaire l'autorise

def test_puissance(parser):
    assert parser.parse("2 ^ 3") == 8.0
    assert parser.parse("9 ^ 0.5") == 3.0  # Racine carrée

def test_priorite_operateurs_et_parentheses(parser):
    # La multiplication prime sur l'addition
    assert parser.parse("2 + 3 * 4") == 14.0
    
    # Les parenthèses forcent la priorité
    assert parser.parse("(2 + 3) * 4") == 20.0
    assert parser.parse("10 / (2 + 3)") == 2.0

def test_variables_internes(parser):
    # Test avec la variable par défaut (pi, e)
    # On utilise pytest.approx car on manipule des float
    assert parser.parse("pi") == pytest.approx(math.pi)
    assert parser.parse("e") == pytest.approx(math.exp(1))
    assert parser.parse("pi * 2") == pytest.approx(math.pi * 2)

def test_variables_personnalisees(parser):
    # On injecte nos propres variables
    assert parser.parse("x + 10", variables={"x": 5}) == 15.0
    assert parser.parse("x * y", variables={"x": 2, "y": 3}) == 6.0
    
    # Surcharge d'une variable interne (ex: on redéfinit pi)
    assert parser.parse("pi", variables={"pi": 3.14}) == 3.14

def test_erreurs_syntaxe(parser):
    # Erreur de parsing Lark (syntaxe invalide)
    with pytest.raises(LarkError):
        parser.parse("2 + * 3")
        
    with pytest.raises(LarkError):
        parser.parse("abc +")
