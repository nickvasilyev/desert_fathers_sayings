#!/bin/bash
zip -u skill.zip desert_fathers.py
zip -u skill.zip desert_father_sayings.json
zip -u skill.zip desert_father_sayings_v2.json
zip -u skill.zip sayings.py
cd skill_env/lib/python3.6/site-packages/ ; zip -ur ../../../../skill.zip *; cd ../../../../
aws lambda update-function-code --function-name alexa_skill_1 --zip-file fileb://skill.zip
