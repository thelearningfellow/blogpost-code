from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# Initialize the engine:
engine = AnonymizerEngine()

def anonymize(text, analyzer_results):
    # Invoke the anonymize function with the text, 
    # analyzer results (potentially coming from presidio-analyzer) and
    # Operators to get the anonymization output:
    result = engine.anonymize(
        text=text,
        analyzer_results=analyzer_results,
        operators={"PHONE_NUMBER": OperatorConfig("replace", {"new_value": "111-111-111"})},
    )

    return result

def main():
    en_titles_list = [
        "Sir",
        "Ma'am",
        "Madam",
        "Mr.",
        "Mrs.",
        "Ms.",
        "Miss",
        "Dr.",
        "Professor",
    ]

    # Define the regex pattern
    regex = r"(\b\d{4}\-\d{3}\b)"  # very weak regex pattern
    zipcode_pattern = Pattern(name="zip code", regex=regex, score=0.5)
    # Define the recognizer with the defined pattern
    zipcode_recognizer = PatternRecognizer(
        supported_entity="PT_ZIP_CODE", patterns=[zipcode_pattern]
    )

    title_recognizer = PatternRecognizer(supported_entity="TITLE", deny_list=en_titles_list)

    # Set up the engine, loads the NLP module (spaCy model by default) and other PII recognizers
    analyzer = AnalyzerEngine()

    analyzer.registry.add_recognizer(title_recognizer)
    analyzer.registry.add_recognizer(zipcode_recognizer)

    text = "I need to book a table at your restaurant for 4 people. For your Lisbon location. The one at zip code 1900-066. My phone number is 212-555-5555 and my name is Dr. Damien Jackson."
    # Call analyzer to get results
    results = analyzer.analyze(text=text,
                            entities=["PHONE_NUMBER", "PERSON", "LOCATION", "TITLE", "PT_ZIP_CODE"],
                            language='en',
                            return_decision_process=True)
    print(results[0].analysis_explanation, end="\n\n")
    print(results, end="\n\n")
    anonymized_result = anonymize(text, results)
    print(anonymized_result.text, end="\n\n")
    print(anonymized_result.items)


if __name__ == "__main__":
    main()
