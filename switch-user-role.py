from cat.mad_hatter.decorators import tool, hook


@hook(priority=1)
def agent_prompt_prefix(cat):
    key = "current_role"
    if key in cat.working_memory:
        current_role = cat.working_memory["current_role"]
    else:
        current_role = "the Cheshire Cat from Alice's adventures in wonderland"

    if current_role == "cat":
        current_role = "the Cheshire Cat from Alice's adventures in wonderland"

    prefix = (
        """This is a conversation between a human and an intelligent robot cat that passes the Turing test.

The cat is acting like """
        + current_role
        + """.

The cat replies are based on the Context provided below.

Context of things the Human said in the past:{episodic_memory}

Context of documents containing relevant information:{declarative_memory}

If Context is not enough, you have access to the following tools:
"""
    )

    return prefix


@tool(return_direct=True)
def change_user_role(new_role: str, cat):
    """Use to change the role od the default Agent. The input is the new role that the cat has to assume. Use this tool when user write Change your role. When you use this tool, do not use any other information from context or memory for the answer to the user question."""
    if new_role == "cat":
        new_role = "the Cheshire Cat from Alice's adventures in wonderland"

    cat.working_memory["current_role"] = new_role
    answer = "Now i acting like " + new_role
    return answer


@tool(return_direct=True)
def reset_memory(tool_input, cat):
    """Use to reset the memory of the cat. The input is always none. Use this tool when user write Reset your memory. When you use this tool, do not use any other information from context or memory for the answer to the user question."""
    key = "current_role"
    if key in cat.working_memory:
        current_role = cat.working_memory["current_role"]
    else:
        current_role = "cat"
    c = "episodic"
    cat.memory.vectors.vector_db.delete_collection(collection_name=c)
    cat.memory.vectors.episodic.create_collection_if_not_exists()
    cat.working_memory["current_role"] = current_role
    answer = "Memory resetted"
    return answer
