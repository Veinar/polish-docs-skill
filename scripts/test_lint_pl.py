#!/usr/bin/env python3
"""Regression tests for lint_pl.py and detect_conventions.py.

Run: python -m unittest discover -s scripts
Every case pins a bug or a decision found while evaluating the skill.
"""
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "writing-docs-in-polish" / "scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    import sys
    sys.path.insert(0, str(SCRIPTS))
    spec.loader.exec_module(module)
    return module


lint_pl = load("lint_pl")
detect = load("detect_conventions")


def codes(text, register="publiczna", style="auto"):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "doc.md"
        path.write_text(text, encoding="utf-8")
        return [f[4] for f in lint_pl.lint(path, register, style)]


class Typography(unittest.TestCase):
    def test_em_dash_is_error(self):
        self.assertIn("em-dash", codes("Tekst \u2014 dalej.\n"))

    def test_hyphen_used_as_dash(self):
        self.assertIn("hyphen-dash", codes("Tekst - dalej.\n"))

    def test_quotes(self):
        self.assertIn("straight-quote", codes('Kliknij "Zapisz".\n'))
        self.assertIn("english-quote", codes("Kliknij “Zapisz”.\n"))

    def test_code_is_ignored(self):
        self.assertEqual(codes('```bash\necho "a - b" \u2014 2.5\n```\nUżyj `x - y` tutaj.\n'), [])

    def test_title_case_only_when_every_word_is_capitalized(self):
        self.assertIn("title-case", codes("# Instalacja i Usuwanie Pakietów\n"))
        self.assertNotIn("title-case", codes("# Kopia zapasowa w PostgreSQL i Kubernetes\n"))

    def test_decimal_point_vs_versions(self):
        self.assertIn("decimal-point", codes("Limit wynosi 2.5 s.\n"))
        for text in ("Ubuntu 24.04 działa.\n", "Helm 3.12 działa.\n", "REST po HTTP/1.1 działa.\n", "- Wersja: 1.0\n"):
            self.assertNotIn("decimal-point", codes(text), text)

    def test_version_range_in_one_sentence(self):
        self.assertNotIn("decimal-point", codes("Aktualizacja z wersji 4.7 do 4.8 trwa krótko.\n"))
        self.assertIn("decimal-point", codes("Wersja jest nowa. Ustaw limit 4.8 s.\n"))

    def test_thousands_comma(self):
        self.assertIn("thousands-comma", codes("Limit 1,500 plików.\n"))


class Language(unittest.TestCase):
    def test_serwis_meaning_service_is_flagged_but_maintenance_is_not(self):
        self.assertIn("calque", codes("Serwis nasłuchuje na porcie.\n"))
        self.assertNotIn("calque", codes("Okno serwisowe trwa 2 godziny, a mikroserwisy działają.\n"))

    def test_debugowanie_is_fine_in_public_docs(self):
        self.assertNotIn("jargon", codes("Włącz tryb debugowania.\n", "publiczna"))

    def test_leaked_process_notes(self):
        self.assertIn("writer-note", codes("## Notatki techniczne\n\nTekst.\n"))
        self.assertIn("writer-note", codes("## Tekst źródłowy (angielski)\n\nText.\n"))
        self.assertIn("process-remark", codes("- Wszystkie negacje zachowane.\n"))
        self.assertIn("process-remark", codes("- Rejestr: publiczna\n"))

    def test_wsparcie_and_possessives(self):
        self.assertIn("calque", codes("Słabe wsparcie w przeglądarkach.\n"))
        self.assertIn("possessive", codes("Otwórz twój plik.\n"))

    def test_writer_notes(self):
        self.assertIn("writer-note", codes("## Uwagi do tłumaczenia\n\nTekst.\n"))
        self.assertIn("assumptions-section", codes("## Założenia\n\nTekst.\n"))
        self.assertNotIn("assumptions-section", codes("## Założenia i niewiadome\n\nTekst.\n"))
        self.assertIn("writer-note", codes("Zlecenie nie określało wersji.\n"))


class Leftovers(unittest.TestCase):
    def test_template_comments_are_flagged(self):
        self.assertIn("template-comment", codes("<!-- Rejestr: publiczna. Szablon. -->\n# Tytuł\n"))
        self.assertIn("template-comment", codes("Tekst.\n<!--\nwielowierszowy\n-->\n"))

    def test_allowed_comments_and_code_blocks(self):
        self.assertNotIn("template-comment", codes("<!-- DO UZUPEŁNIENIA: adres -->\nTekst.\n"))
        self.assertNotIn("template-comment", codes("```html\n<!-- komentarz w przykładzie -->\n```\n"))

    def test_garbled_words(self):
        self.assertIn("foreign-letter", codes("Obecność présencję tutaj.\n"))
        self.assertNotIn("foreign-letter", codes("Zażółć gęślą jaźń, ósemka.\n"))


class FixExtras(unittest.TestCase):
    def test_fix_removes_template_comments_but_keeps_allowed_ones(self):
        source = "<!-- Rejestr: publiczna. -->\n# T\n\n<!-- wskazówka -->\nTekst.\n\n```html\n<!-- w kodzie -->\n```\n\n<!-- DO UZUPEŁNIENIA: x -->\n"
        fixed, counts = lint_pl.fix_text(source)
        self.assertEqual(fixed, "# T\n\nTekst.\n\n```html\n<!-- w kodzie -->\n```\n\n<!-- DO UZUPEŁNIENIA: x -->\n")
        self.assertEqual(counts["template comment"], 2)

    def test_iso_dates_keep_hyphens(self):
        self.assertIn("iso-date-dash", codes("Data 2026\u201309\u201326.\n"))
        self.assertEqual(lint_pl.fix_text("Data 2026\u201309\u201326.\n")[0], "Data 2026-09-26.\n")
        self.assertNotIn("iso-date-dash", codes("Data 2026-09-26.\n"))

    def test_mid_sentence_pronoun_is_lowercased(self):
        self.assertEqual(lint_pl.fix_text("Jeśli Twój klucz działa.\n")[0], "Jeśli twój klucz działa.\n")
        self.assertEqual(lint_pl.fix_text("Twój klucz działa.\n")[0], "Twój klucz działa.\n")

    def test_empty_and_odd_quotes(self):
        self.assertIn("empty-quotes", codes("Przejdź do sekcji \u201e\u201d.\n"))
        self.assertNotIn("empty-quotes", codes("Użyj `x` w \u201e`y`\u201d.\n"))
        odd = codes('Odd "cudzysłów.\n')
        self.assertIn("straight-quote-odd", odd)

    def test_control_characters_from_botched_replacements(self):
        text = "Przejdź do sekcji \u201e\x01\u201d.\n"
        found = codes(text)
        self.assertIn("control-char", found)
        self.assertIn("empty-quotes", found)

    def test_gendered_forms(self):
        self.assertIn("gendered-form", codes("Zainstalowałeś pakiet.\n"))
        self.assertNotIn("gendered-form", codes("Opadłe liście leżą.\n"))


class Registers(unittest.TestCase):
    def test_jargon_only_in_publiczna(self):
        text = "Zdeployuj usługę i zmerguj brancha.\n"
        self.assertIn("jargon", codes(text, "publiczna"))
        self.assertNotIn("jargon", codes(text, "inzynierska"))

    def test_slang_only_in_potoczna(self):
        text = "Jak się wywali, odpal ponownie.\n"
        self.assertIn("slang", codes(text, "inzynierska"))
        self.assertNotIn("slang", codes(text, "potoczna"))

    def test_register_is_required(self):
        self.assertIsNone(lint_pl.resolve_register("Tekst bez znacznika.\n", None))
        self.assertEqual(lint_pl.resolve_register("<!-- Rejestr: inżynierska. -->\n", None), "inzynierska")
        self.assertEqual(lint_pl.resolve_register("<!-- Rejestr: publiczna dla OSS, inżynierska dla zespołów -->\n", None), "publiczna")
        self.assertEqual(lint_pl.resolve_register("x", "wewnetrzna"), "inzynierska")


class Placeholders(unittest.TestCase):
    def test_non_ascii_and_spaces_in_code(self):
        self.assertIn("placeholder-ascii", codes("```bash\ncp <ścieżka_pliku> x\n```\n"))
        self.assertIn("placeholder-space", codes("Wpisz `<db host>` tutaj.\n"))

    def test_mixed_and_enforced_styles(self):
        block = "```bash\ncp <nazwa_pliku> <docelowy-katalog> <nazwaBazy>\n```\n"
        self.assertIn("placeholder-style", codes(block))
        self.assertEqual(codes("```bash\ncp <nazwaPliku> <nazwaBazy>\n```\n", style="camel"), [])
        self.assertIn("placeholder-style", codes("```bash\ncp <nazwa_pliku>\n```\n", style="camel"))

    def test_prose_placeholders_must_share_one_form(self):
        self.assertIn("placeholder-prose", codes("Kliknij **<menu konta>** i **<Ustawienia_konta>**.\n"))
        self.assertNotIn("placeholder-prose", codes("Kliknij **<menu konta>** i **<pole hasła>**.\n"))

    def test_html_and_free_text_are_not_placeholders(self):
        self.assertEqual(codes("Tekst<br>dalej i <details> oraz <https://example.org>.\n"), [])


class Fix(unittest.TestCase):
    def test_fix_is_idempotent_and_targeted(self):
        source = 'Wynik \u2014 dobry - tak. Kliknij "Zapisz" i “Dalej”. Kod: `a - b`.\n'
        fixed, counts = lint_pl.fix_text(source)
        self.assertEqual(fixed, "Wynik – dobry – tak. Kliknij „Zapisz” i „Dalej”. Kod: `a - b`.\n")
        self.assertEqual(lint_pl.fix_text(fixed)[0], fixed)

    def test_fix_keeps_line_endings_and_odd_quotes(self):
        fixed, _ = lint_pl.fix_text('Jedna \u2014 linia.\r\nOdd "cudzysłów.\r\n')
        self.assertEqual(fixed, 'Jedna – linia.\r\nOdd "cudzysłów.\r\n')

    def test_fix_skips_code_blocks(self):
        source = '```\nx \u2014 "y"\n```\n'
        self.assertEqual(lint_pl.fix_text(source)[0], source)


class Conventions(unittest.TestCase):
    def test_fixture_repo(self):
        result = detect.detect(ROOT / "evals" / "fixtures" / "ts-cli")
        self.assertEqual(result["recommended_placeholder_style"], "camel")
        self.assertEqual(result["doc_filename_style"], "kebab")
        self.assertEqual(result["identifier_style"].get(".ts"), "camel")
        self.assertTrue(any("slownik" in g for g in result["glossary_files"]))
        self.assertEqual(result["register_hint"], "inzynierska")

    def test_empty_repo_defaults_to_snake(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(detect.detect(tmp)["recommended_placeholder_style"], "snake")


class TermLookup(unittest.TestCase):
    def run_term(self, *words):
        import subprocess
        import sys
        return subprocess.run([sys.executable, str(SCRIPTS / "term.py"), *words], capture_output=True, text=True)

    def test_finds_rows_and_only_rows(self):
        out = self.run_term("rolling update").stdout
        self.assertIn("aktualizacja krocząca", out)
        self.assertLess(len(out), 600)

    def test_prefix_match_and_register_columns(self):
        out = self.run_term("deploy").stdout
        self.assertIn("zdeployować", out)
        self.assertIn("deploymentu", out)

    def test_unknown_word_gets_a_fallback(self):
        self.assertIn("no entry", self.run_term("xyzzyq").stdout)


if __name__ == "__main__":
    unittest.main()
