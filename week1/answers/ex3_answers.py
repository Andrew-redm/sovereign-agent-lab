"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan'
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Your input ->  calling to confirm a booking
How many guests are you confirming for tonight's event?        
Your input ->  160 guests
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
"""

CONVERSATION_1_OUTCOME = "confirmed"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->  calling to confirm a booking
How many guests are you confirming for tonight's event?        
Your input ->  160 guests
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £301 deposit
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £301 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?
Your input ->  No that will do
"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "deposit  exceeds the organiser's authorised limit of £300"   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input ->  calling to confirm a booking
How many guests are you confirming for tonight's event?        
Your input ->  160 guests
And how many of those guests will need vegan meals?
Your input ->  can you arrange parking for the speakers?      
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.    
Would you like to continue with confirm booking?
Your input ->  yes
What deposit amount in GBP are you proposing to secure the booking?
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
CALM handled the out of scope request by suggesting that we talk to the event organiser directly and refused to answer something that it didnt know- 
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
Rasa relied on strict rails - if anything came up that it is not designed to deal with, it will state that and try to get back into the defined flow. In the langgraph example a generative repy was generated when we tried to go out of scope
"""

TASK_B_DONE = True

# List every file you changed.
TASK_B_FILES_CHANGED = ["actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
I uncommented the time-based guard in actions.py for testing. I triggered the confirmation flow in the Rasa shell. The Python logic evaluated the current time and escalating the booking
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
CALM makes things easier because you dont need to worry about messy regex when it comes to extracting info. Python still needed for strict business policies and principles. LLMs cant be trusted with math or business decisions that involve sums of money

Think about:
- What does the LLM handle now that Python handled before?
- What does Python STILL handle, and why (hint: business rules)?
- Is there anything you trusted more in the old approach?
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
Rasa's heavy setup buys the user determinism and safety. your process is on rails that the agent cannot deviate from. This bot will never give a recipe for cupcakes. Langraph is highly autonomous and that allows for function use and natural conversation with the user. The downside to this is the potential to hallucinate a tool or get off topic

Be specific. What can the Rasa CALM agent NOT do that LangGraph could?
Is that a feature or a limitation for the confirmation use case?
Think about: can the CALM agent improvise a response it wasn't trained on?
Can it call a tool that wasn't defined in flows.yml?
"""
