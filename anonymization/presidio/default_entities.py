from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult, OperatorConfig

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
    

    # Set up the engine, loads the NLP module (spaCy model by default) and other PII recognizers
    analyzer = AnalyzerEngine()

    text = "I need to book the restaurant for 4 people at your Glasgow location. My phone number is 212-555-5555 and my name is Damien Jackson."
    # Call analyzer to get results
    results = analyzer.analyze(text=text,
                            entities=["PHONE_NUMBER", "PERSON", "LOCATION"],
                            language='en',
                            return_decision_process=True)
    print(results[0].analysis_explanation, end="\n\n")
    print(results, end="\n\n")
    anonymized_result = anonymize(text, results)
    print(anonymized_result.text, end="\n\n")
    print(anonymized_result.items)


if __name__ == "__main__":
    main()
