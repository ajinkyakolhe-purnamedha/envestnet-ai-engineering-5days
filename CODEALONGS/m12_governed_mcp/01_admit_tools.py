"""One concept: discovering an MCP tool does not make it model-visible."""

# Imagine an MCP client asked a server which tools it offers.
discovered = {
    "advisor_client_review",
    "export_all_holdings",
}
# Python policy—not the model—chooses which discovered tools this app permits.
approved = {"advisor_client_review"}

# Only this intersection would be supplied to the model as callable tools.
model_visible = sorted(discovered & approved)
# The other tool exists on the server, but this host refuses to expose it.
excluded = sorted(discovered - approved)

print("Discovered:", sorted(discovered))
print("Model-visible:", model_visible)
print("Excluded:", excluded)
