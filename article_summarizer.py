import baseline_model as base_model
import title_bias_model as tb_model
import named_entity_recognition_model as ner_model
import tfidf_model
import mixed_model as m_model

url = input("Enter the URL for the Wikepedia Article you'd like to get the summary for:")
model_modifiers = {}

print("------------------------")
print("Baseline Summary:")
print("------------------------------------------------------------------------------------------------")
original_model_summary = base_model.generate_summary(url)
print(original_model_summary)
print("------------------------------------------------------------------------------------------------")

print(" ")

print("------------------------")
print("Summary Modified to Bias Title Terms:")
print("------------------------------------------------------------------------------------------------")
tb_summary, tb_mods = tb_model.generate_summary(url)
model_modifiers["Title Biased"] = tb_mods
print(tb_summary)
print("------------------------------------------------------------------------------------------------")

print(" ")

print("------------------------")
print("Summary Utilizing Named Entity Recognition:")
print("------------------------------------------------------------------------------------------------")
ner_summary, ner_mods = ner_model.generate_summary(url)
model_modifiers["Named Entity Recognition"] = ner_mods
print(ner_summary)
print("------------------------------------------------------------------------------------------------")

print(" ")

print("------------------------")
print("Summary Utilizing TFIDF:")
print("------------------------------------------------------------------------------------------------")
tfidf_summary, tfidf_mods = tfidf_model.runTFIDF(url)
model_modifiers["TFIDF"] = tfidf_mods
print(tfidf_summary)
print("------------------------------------------------------------------------------------------------")

print(" ")

print("------------------------")
print("Summary Utilizing All of the Above Methods:")
print("------------------------------------------------------------------------------------------------")
mixed_model_summary = m_model.generate_summary(url, model_modifiers["Named Entity Recognition"], model_modifiers["TFIDF"])
print(mixed_model_summary)
print("------------------------------------------------------------------------------------------------")
