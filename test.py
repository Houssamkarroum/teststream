import re
import streamlit as st
import pandas as pd

# === Analyseur lexical ===
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


# === Analyseur syntaxique ===
class MathParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_index = 0

    def current_token(self):
        if self.current_index < len(self.tokens):
            return self.tokens[self.current_index]
        return None

    def advance(self):
        self.current_index += 1

    def match(self, token_type):
        token = self.current_token()
        if token and token[0] == token_type:
            self.advance()
            return token
        return None

    def parse(self):
        result = self.parse_expression()
        if self.current_token():
            raise ValueError("Erreur syntaxique : tokens restants après l'analyse.")
        return result

    def parse_expression(self):
        result = self.parse_term()
        while self.current_token() and self.current_token()[0] in {"OP_ADD", "OP_SUB"}:
            operator = self.match("OP_ADD") or self.match("OP_SUB")
            right = self.parse_term()
            if operator[0] == "OP_ADD":
                result += right
            elif operator[0] == "OP_SUB":
                result -= right
        return result

    def parse_term(self):
        result = self.parse_factor()
        while self.current_token() and self.current_token()[0] in {"OP_MUL", "OP_DIV"}:
            operator = self.match("OP_MUL") or self.match("OP_DIV")
            right = self.parse_factor()
            if operator[0] == "OP_MUL":
                result *= right
            elif operator[0] == "OP_DIV":
                if right == 0:
                    raise ValueError("Erreur sémantique : division par zéro.")
                result /= right
        return result

    def parse_factor(self):
        if self.match("LPAREN"):
            result = self.parse_expression()
            if not self.match("RPAREN"):
                raise ValueError("Erreur syntaxique : parenthèse fermante manquante.")
            return result
        token = self.match("NUMBER")
        if token:
            return int(token[1])
        raise ValueError("Erreur syntaxique : facteur attendu.")


# === Analyseur sémantique ===
class MathSemanticAnalyzer:
    def __init__(self, result):
        self.result = result

    def analyze(self):
        if self.result > 1e6:
            raise ValueError("Erreur sémantique : le résultat dépasse la limite autorisée.")
        return self.result


# === Application Streamlit ===
def main():
    st.set_page_config(page_title="Analyseur Mathématique", page_icon="📊", layout="wide")
    
    # Add the header with 'Made by' text
    st.markdown(
        """
        <div style="text-align:center;">
            <h1>Analyseur Mathématique</h1>
            <p style="font-size:16px; color:gray;">Made by Houssam Karroum & Yassine Hachguer</p>
        </div>
        """, unsafe_allow_html=True)

    # Entrée utilisateur pour l'expression mathématique
    input_expression = st.text_input("Entrez une expression mathématique :", "5 + (6 * 2) - (3 - 8)")

    if input_expression:
        # --- Analyse lexicale ---
        lexer = MathLexer()
        tokens = lexer.tokenize(input_expression)

        # --- Affichage des Tokens ---
        tokens_df = pd.DataFrame(tokens, columns=["Type", "Valeur"])
        st.subheader("Tokens Extraits")
        st.table(tokens_df)

        # --- Analyse syntaxique ---
        parser = MathParser(tokens)
        try:
            result = parser.parse()

            # --- Analyse sémantique ---
            semantic_analyzer = MathSemanticAnalyzer(result)
            final_result = semantic_analyzer.analyze()

            # --- Affichage des résultats ---
            st.subheader("Résultats de l'Analyse")
            st.markdown(f"**Expression Saisie** : `{input_expression}`")
            st.markdown(f"**Résultat Final** : `{final_result}`")
        
        except ValueError as e:
            st.error(f"Erreur : {e}")

# Exécution de l'application Streamlit
if __name__ == "__main__":
    main()
