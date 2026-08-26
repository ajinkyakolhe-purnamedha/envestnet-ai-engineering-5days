from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from common import chat, retrieve
from llama_index.core.tools import FunctionTool


def search_policy(question: str) -> str:
    documents = [{"source": "limit", "text": "AAPL and every other single-stock allocation may not exceed 35 percent."}, {"source": "cash", "text": "Cash supports short-term liquidity."}]
    winner = retrieve(question, documents, 1)[0]
    return f"source={winner['source']}; text={winner['text']}"


def main() -> None:
    tool = FunctionTool.from_defaults(fn=search_policy)
    question = "Can Alice raise AAPL to 36 percent?"
    source = str(tool.call(question=question))
    print("RAG tool source:", source)
    print("Grounded answer:", chat([{"role": "user", "content": f"Tool result: {source}\nQuestion: {question}"}], 40))


if __name__ == "__main__":
    main()
