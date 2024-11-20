import re
import streamlit as st


class MathLexer:
    rules = [
        ("NUMBER", r"\d+"),                 # Constante entière
        ("OP_ADD", r"\+"),                  # Opérateur d'addition
        ("OP_SUB", r"-"),                   # Opérateur de soustraction
        ("OP_MUL", r"\*"),                  # Opérateur de multiplication
        ("OP_DIV", r"/"),                   # Opérateur de division
        ("LPAREN", r"\("),                  # Parenthèse ouvrante
        ("RPAREN", r"\)"),                  # Parenthèse fermante
        ("WHITESPACE", r"[ \t]+"),          # Espaces (à ignorer)
    ]

    def __init__(self):
        self.tokens = []

    def tokenize(self, text):
        position = 0
        while position < len(text):
            match = None
            for token_name, token_regex in self.rules:
                regex = re.compile(token_regex)
                match = regex.match(text, position)
                if match:
                    value = match.group(0)
                    if token_name != "WHITESPACE":  # On ignore les espaces
                        self.tokens.append((token_name, value))
                    position += len(value)
                    break
            if not match:
                raise ValueError(f"Erreur lexicale : caractère inattendu '{text[position]}'")
        return self.tokens


class MathParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def parse(self):
        """Parse l'expression mathématique."""
        if not self.tokens:
            raise ValueError("Aucune expression à analyser.")
        result = self._expression()
        if self.current_token_index < len(self.tokens):
            raise ValueError("Erreur syntaxique : jetons restants après l'analyse.")
        return result

    def _expression(self):
        """Parse une expression : term ((+|-) term)*"""
        result = self._term()
        while self._current_token() and self._current_token()[0] in {"OP_ADD", "OP_SUB"}:
            operator = self._consume()[1]
            right = self._term()
            if operator == "+":
                result += right
            elif operator == "-":
                result -= right
        return result

    def _term(self):
        """Parse un terme : factor ((|/) factor)"""
        result = self._factor()
        while self._current_token() and self._current_token()[0] in {"OP_MUL", "OP_DIV"}:
            operator = self._consume()[1]
            right = self._factor()
            if operator == "*":
                result *= right
            elif operator == "/":
                if right == 0:
                    raise ValueError("Division par zéro.")
                result /= right
        return result

    def _factor(self):
        """Parse un facteur : NUMBER | (expression)"""
        token = self._current_token()
        if token[0] == "NUMBER":
            return int(self._consume()[1])
        elif token[0] == "LPAREN":
            self._consume()  # Consommer '('
            result = self._expression()
            if self._current_token()[0] != "RPAREN":
                raise ValueError("Parenthèse fermante manquante.")
            self._consume()  # Consommer ')'
            return result
        else:
            raise ValueError(f"Erreur syntaxique : attendu un nombre ou une parenthèse, trouvé {token}.")

    def _current_token(self):
        """Retourne le jeton courant."""
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None

    def _consume(self):
        """Consomme et retourne le jeton courant."""
        token = self._current_token()
        if token:
            self.current_token_index += 1
        return token


class SemanticAnalyzer:
    @staticmethod
    def analyze(tokens):
        # Vérifier que les parenthèses sont équilibrées
        balance = 0
        for token_type, value in tokens:
            if token_type == "LPAREN":
                balance += 1
            elif token_type == "RPAREN":
                balance -= 1
            if balance < 0:
                raise ValueError("Analyse sémantique : parenthèses non équilibrées.")
        if balance != 0:
            raise ValueError("Analyse sémantique : parenthèses non équilibrées.")

        # Vérification des divisions par zéro
        for i, (token_type, value) in enumerate(tokens):
            if token_type == "OP_DIV":
                if i + 1 < len(tokens) and tokens[i + 1][0] == "NUMBER" and int(tokens[i + 1][1]) == 0:
                    raise ValueError("Analyse sémantique : division par zéro détectée.")
        return "Aucune erreur sémantique détectée."


# Interface Streamlit
st.title("Analyseur Mathématique")
st.markdown("*Entrez une expression mathématique pour l'analyser et l'évaluer.*")

input_expression = st.text_input("Expression mathématique", value="5 + (6*2)")

if st.button("Analyser"):
    try:
        lexer = MathLexer()
        tokens = lexer.tokenize(input_expression)
        st.subheader("Analyse Lexicale")
        st.write("Tokens extraits :", tokens)

        # Analyse sémantique
        analyzer = SemanticAnalyzer()
        semantic_result = analyzer.analyze(tokens)
        st.subheader("Analyse Sémantique")
        st.success(semantic_result)

        # Analyse syntaxique et évaluation
        parser = MathParser(tokens)
        result = parser.parse()
        st.subheader("Résultat de l'évaluation")
        st.success(f"Résultat : {result}")

    except ValueError as e:
        st.error(f"Erreur : {e}")
