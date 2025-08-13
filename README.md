# unify-mcp

Turn discussion into action.

How much valuable information is buried in your Slack history?
Is your documentation actually reflecting the latest decisions, or is it falling behind?

This AI assistant listens to your team’s conversations, identifies tasks and key ideas, and automatically updates your documentation and project management tools so nothing gets lost. Say goodbye to manual updates and missed details. Your team stays focused, aligned, and productive, and every decision, task, and insight is captured and acted on instantly. 

Goals:
Agent Capabilities
 - [X] Manage Trello Board
    - [X] When a user reports a task's completion, it is moved to the "Done" list
    - [X] When a user assigns a task to another person, that person is assigned in trello card
    - [X] When a user discusses a task, any additional details are added to the task's description or checklist
 - [X] Research Topics
    - [X] Go through the history of a trello board, finding and storing common checklists
    - [X] Reuse previous checklists instead of creating new ones
 - [X] Documentation (Google Docs)
    - [X] Update documentation & trello with new information (Asks user permission first)
    - [X] When a card is created add relavent links to documentation

### References:

https://openai.github.io/openai-agents-python/

https://developer.atlassian.com/cloud/trello/rest/api-group-actions/#api-group-actions

https://gofastmcp.com/
