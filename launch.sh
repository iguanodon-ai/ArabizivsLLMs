lang=$1
echo "Prompt language: $lang"
for dialect in lebanon_north lebanon_south algeria_algiers algeria_constantine egypt_cairo egypt_louxour
    do
        echo "Dialect: $dialect"
        #python main.py translate --dialect $dialect --model gpt4o --promptlang $lang
        #echo "Done for gpt4o"
        #python main.py translate --dialect $dialect --model claude3 --promptlang $lang
        #echo "Done for claude3"
        #python main.py translate --dialect $dialect --model llama3 --promptlang $lang
        #echo "Done for llama3"
        #python main.py translate --dialect $dialect --model gemma2 --promptlang $lang
        #echo "Done for gemma2"
        #python main.py translate --dialect $dialect --model mistrallarge --promptlang $lang
        #echo "Done for mistrallarge"
        #python main.py translate --dialect $dialect --model jais --promptlang $lang
        #echo "Done for jais"
        python main.py translate --dialect $dialect --model gemini --promptlang $lang
        echo "Done for gemini"
    done