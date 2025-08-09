import pdfplumber
import json
from typing import Dict, List, Optional
import re

class PDFParser:
    def __init__(self):
        self.semester_pattern = re.compile(r'^\|?(\d+)\s*\|')
        self.discipline_pattern = re.compile(r'^\|?\d*\s*\|([^|]+)\|([^|]+)\|([^|]+)\|?')

    def parse_pdf(self, pdf_path: str) -> Dict[str, List[Dict]]:
        data = {}
        current_semester = None
        current_block = None

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue

                for line in text.split('\n'):
                    line = line.strip()
                    if not line:
                        continue

                    if "Обязательные дисциплины" in line:
                        current_block = "Обязательные"
                    elif "Пул выборных дисциплин" in line:
                        current_block = "Выборные"

                    semester_match = self.semester_pattern.search(line)
                    if semester_match:
                        current_semester = f"Семестр {semester_match.group(1)}"
                        if current_semester not in data:
                            data[current_semester] = {
                                "Обязательные": [],
                                "Выборные": []
                            }

                    if current_semester and "|" in line:
                        discipline_match = self.discipline_pattern.search(line)
                        if discipline_match:
                            name = discipline_match.group(1).strip()
                            if name and not name.isdigit():
                                discipline = {
                                    "name": name,
                                    "workload_units": discipline_match.group(2).strip(),
                                    "workload_hours": discipline_match.group(3).strip(),
                                    "type": current_block if current_block else "Другое"
                                }
                                if current_block:
                                    data[current_semester][current_block].append(discipline)
                                else:
                                    if "Другое" not in data[current_semester]:
                                        data[current_semester]["Другое"] = []
                                    data[current_semester]["Другое"].append(discipline)

        return data

    def create_knowledge_base(self, parsed_data: Dict, output_path: str) -> None:
        knowledge_base = {
            "program_name": "Управление ИИ-продуктами" if "10130" in output_path else "Искусственный интеллект",
            "semesters": [],
            "statistics": {
                "total_disciplines": 0,
                "mandatory_count": 0,
                "elective_count": 0
            }
        }

        for semester, disciplines in parsed_data.items():
            semester_data = {
                "semester": semester,
                "mandatory": disciplines.get("Обязательные", []),
                "elective": disciplines.get("Выборные", []),
                "other": disciplines.get("Другое", [])
            }
            
            knowledge_base["semesters"].append(semester_data)
            knowledge_base["statistics"]["total_disciplines"] += (
                len(semester_data["mandatory"]) + 
                len(semester_data["elective"]) + 
                len(semester_data["other"])
            )
            knowledge_base["statistics"]["mandatory_count"] += len(semester_data["mandatory"])
            knowledge_base["statistics"]["elective_count"] += len(semester_data["elective"])

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(knowledge_base, f, ensure_ascii=False, indent=2)

def main():
    parser = PDFParser()
    
    ai_product_data = parser.parse_pdf("10130-abit.pdf")
    parser.create_knowledge_base(ai_product_data, "ai_product_knowledge_base.json")
    
    ai_data = parser.parse_pdf("10033-abit.pdf")
    parser.create_knowledge_base(ai_data, "ai_knowledge_base.json")

    print("Базы знаний успешно созданы:")
    print("- ai_product_knowledge_base.json")
    print("- ai_knowledge_base.json")

if __name__ == "__main__":
    main()