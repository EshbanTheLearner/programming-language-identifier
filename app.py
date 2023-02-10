import streamlit as st
from transformers import RobertaForSequenceClassification, RobertaTokenizer, TextClassificationPipeline

st.set_page_config(page_title="Programming Language Identifier", page_icon="🕵🏽", initial_sidebar_state="auto")

code_snippets_list = [
    """
    def square(value):
        return square**2
    """.lstrip(),
    """
    package main
    import "fmt"
    func main() {
        fmt.Println("Hello World!")
    }
    """.lstrip(),
    """
    public static <mask> set(string $key, $value) {
        if (!in_array($key, self::$allowedKeys)) {
            throw new \InvalidArgumentException('Invalid key given');
        }
        self::$storedValues[$key] = $value;
    }
    """.lstrip(),
    """
    function fibonacci(num){   
        if(num==1)
            return 0;
        if (num == 2)
            return 1;
        return fibonacci(num - 1) + fibonacci(num - 2);
    }
    """.lstrip(),
    """
    def mutate(array)
        array.pop
    end
    """.lstrip()
]

code_snippets = {
    "Python": code_snippets_list[0],
    "Go": code_snippets_list[1],
    "PHP": code_snippets_list[2],
    "Javascript": code_snippets_list[3],
    "Ruby": code_snippets_list[4]
}

st.cache(show_spinner=True)
def load_pipeline():
    pipeline = TextClassificationPipeline(
        model=RobertaForSequenceClassification.from_pretrained("huggingface/CodeBERTa-language-id"),
        tokenizer=RobertaTokenizer.from_pretrained("huggingface/CodeBERTa-language-id")
    )
    return pipeline

pipeline = load_pipeline()

st.header("Programming Langauge Identifier")
st.subheader("Paste your code snippet below 👇🏽")

selected_code_snippet = st.selectbox(
    "Select a random code snippet",
    code_snippets.keys()
)

text = st.text_area(
    label="", 
    value=code_snippets[selected_code_snippet],
    height=250,
    max_chars=None,
    key=None
)

button = st.button("Detect Language 🔎")

if button:
    if not len(text) == 0:
        result_dict = pipeline(text)[0]
        st.write(result_dict["label"])
    else:
        st.write("Add some text please")