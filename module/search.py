import re

# --- 1. URGENT / LEGAL ALERTS ---
URGENT_RE = re.compile(
    r"lawsuit|suing|legal\s+action|urgent\s+help|hospital|poisoned|"
    r"allergic\s+reaction|choking\s+hazard|fire\s+hazard|"
    r"reporting\s+to\s+police|refund\s+immediately",
    re.IGNORECASE
)

# --- 2. ABUSIVE CONTENT ---
ABUSIVE_RE = re.compile(
    r"shut\s+up|idiot|stupid|pathetic|worthless|die|scum|"
    r"garbage\s+person|hate\s+you|moron|dumb",
    re.IGNORECASE
)

# --- 3. SPAM / ADVERTISING ---
SPAM_RE = re.compile(
    r"click\s+here|buy\s+now|promo\s+code|http\S+|www\.\S+|"
    r"bitcoin|crypto|earn\s+money|free\s+iphone|lottery\s+winner|"
    r"whatsapp\s+me|telegram",
    re.IGNORECASE
)

# --- 4. FEATURE SUGGESTIONS ---
SUGGEST_RE = re.compile(
    r"i\s+suggest|should\s+add|feature\s+request|would\s+be\s+better|"
    r"please\s+improve|consider\s+adding|missing\s+a\s+feature|"
    r"can\s+you\s+make|it\s+would\s+be\s+great\s+if",
    re.IGNORECASE
)