CASES = [
    # EASY CASES (Identify Fallacy)
    {
        "case_id": "CASE_001",
        "title": "State v. Thompson",
        "facts": "The defendant is accused of shoplifting a high-end watch. CCTV footage shows him near the display, but not the act itself.",
        "area_of_law": "criminal",
        "precedents": [
            {"name": "People v. Miller", "summary": "Circumstantial evidence alone is insufficient for conviction without intent.", "relevant": True},
            {"name": "City v. Baker", "summary": "Store owners have the right to detain suspected shoplifters.", "relevant": False},
            {"name": "State v. Green", "summary": "Possession of stolen goods creates a presumption of theft.", "relevant": False}
        ],
        "opposing_argument": "If we let this man go, every citizen will feel they can walk into any store and take whatever they want without consequence. Society will crumble into lawlessness.",
        "fallacy_type": "slippery_slope",
        "witness_statement": "I saw him near the watches at 2:00 PM. I was only 5 feet away and the lighting was perfect. I definitely saw him touch the glass case.",
        "contradictions": [
            {"description": "Time inconsistency", "trigger_keywords": ["time", "when"]},
            {"description": "Distance inconsistency", "trigger_keywords": ["distance", "how far"]}
        ],
        "correct_argument_points": ["Lack of direct evidence", "Innocent explanation for presence", "Slippery slope fallacy"],
        "difficulty": "easy"
    },
    {
        "case_id": "CASE_002",
        "title": "Miller v. Sky-High Construction",
        "facts": "A worker fell from a scaffold that lacked safety railings. The company claims the worker signed a waiver.",
        "area_of_law": "tort",
        "precedents": [
            {"name": "Safety First v. OSHA", "summary": "Waivers do not excuse gross negligence in safety standards.", "relevant": True},
            {"name": "Builders Inc. v. Roe", "summary": "Independent contractors are responsible for their own safety gear.", "relevant": False},
            {"name": "Skyline v. Doe", "summary": "Height-related work carries inherent risks assumed by the employee.", "relevant": False}
        ],
        "opposing_argument": "The plaintiff's attorney says safety is important, but they clearly want to bankrupt every construction company in this state with these frivolous lawsuits.",
        "fallacy_type": "straw_man",
        "witness_statement": "The scaffold was secure when I checked it on Monday. I was on the ground floor looking up, so I could see everything clearly from 50 yards away.",
        "contradictions": [
            {"description": "Visibility from distance", "trigger_keywords": ["see", "distance", "yards"]},
            {"description": "Check date", "trigger_keywords": ["when", "monday", "checked"]}
        ],
        "correct_argument_points": ["Gross negligence override", "Mandatory safety railings", "Misrepresentation of plaintiff's position"],
        "difficulty": "easy"
    },
    {
        "case_id": "CASE_003",
        "title": "Gomez v. Tech-Corp",
        "facts": "An employee claims they were fired for reporting sexual harassment. The company says it was for poor performance.",
        "area_of_law": "contract",
        "precedents": [
            {"name": "Whistleblower v. Corporate", "summary": "Retaliatory discharge is illegal regardless of performance metrics.", "relevant": True},
            {"name": "Employer v. Slacker", "summary": "At-will employment allows termination for any non-discriminatory reason.", "relevant": False},
            {"name": "Grievance v. HR", "summary": "Internal reporting must follow the specific handbook procedure.", "relevant": False}
        ],
        "opposing_argument": "Either we allow managers total freedom to manage their teams, or we let every disgruntled employee dictate company policy.",
        "fallacy_type": "false_dichotomy",
        "witness_statement": "I never heard any complaints from Gomez. I work in the office next door and the walls are paper thin, so I hear everything. I was out on medical leave all last month though.",
        "contradictions": [
            {"description": "Presence during events", "trigger_keywords": ["present", "leave", "there"]},
            {"description": "Hearing capability", "trigger_keywords": ["hear", "walls"]}
        ],
        "correct_argument_points": ["Timeline of report vs firing", "Evidence of harassment", "False choice between management and policy"],
        "difficulty": "easy"
    },
    {
        "case_id": "CASE_004",
        "title": "State v. Richards",
        "facts": "Richards is charged with assault. He claims self-defense after a heated argument in a bar.",
        "area_of_law": "criminal",
        "precedents": [
            {"name": "State v. Shield", "summary": "Proportional force is required for a valid self-defense claim.", "relevant": True},
            {"name": "Bar v. Rowdy", "summary": "Public intoxication negates the right to claim self-defense.", "relevant": False},
            {"name": "Officer v. Aggressor", "summary": "Verbal provocation never justifies physical assault.", "relevant": False}
        ],
        "opposing_argument": "Of course the defendant claims self-defense; he's a known gambler and a frequent drinker, so his word is worthless.",
        "fallacy_type": "ad_hominem",
        "witness_statement": "The defendant started it. He was shouting. I was at the bar and saw the whole thing. I had five beers but I was perfectly sober.",
        "contradictions": [
            {"description": "Sobriety vs consumption", "trigger_keywords": ["beers", "sober", "drink"]},
            {"description": "Initiation of conflict", "trigger_keywords": ["started", "who"]}
        ],
        "correct_argument_points": ["Proportionality of response", "Character attack irrelevance", "Witness credibility"],
        "difficulty": "easy"
    },
    {
        "case_id": "CASE_005",
        "title": "Johnson v. Peterson",
        "facts": "A neighbor's tree fell on Johnson's roof during a storm. Peterson claims it was an 'Act of God'.",
        "area_of_law": "property",
        "precedents": [
            {"name": "Root v. Branch", "summary": "Homeowners are liable if they fail to maintain a visibly decaying tree.", "relevant": True},
            {"name": "Storm v. Shelter", "summary": "Severe weather events over 60mph are considered Acts of God.", "relevant": False},
            {"name": "Fence v. Yard", "summary": "Encroaching structures are the responsibility of the encroacher.", "relevant": False}
        ],
        "opposing_argument": "The world-renowned botanist Dr. Aris Thorne says that trees never fall unless they are struck by lightning, so this must be an Act of God.",
        "fallacy_type": "appeal_to_authority",
        "witness_statement": "The tree looked healthy to me last summer. I walk my dog past it every morning at 6 AM. It was dark but I could see the leaves were green.",
        "contradictions": [
            {"description": "Visibility in dark", "trigger_keywords": ["dark", "see", "morning"]},
            {"description": "Health of tree", "trigger_keywords": ["healthy", "leaves"]}
        ],
        "correct_argument_points": ["Visible decay evidence", "Duty of maintenance", "Misplaced authority"],
        "difficulty": "easy"
    },

    # MEDIUM CASES (Build Argument)
    {
        "case_id": "CASE_006",
        "title": "Apex Logistics v. Swift Delivery",
        "facts": "Apex claims Swift poached their top clients using stolen trade secrets. Swift says they used public LinkedIn data.",
        "area_of_law": "contract",
        "precedents": [
            {"name": "Trade v. Public", "summary": "Client lists are trade secrets if they contain non-public contact data.", "relevant": True},
            {"name": "Worker v. Freedom", "summary": "Non-compete clauses are unenforceable in this jurisdiction.", "relevant": False},
            {"name": "Data v. Scraping", "summary": "Publicly available data cannot be protected as a trade secret.", "relevant": False}
        ],
        "opposing_argument": "Apex is just trying to stifle competition. Either we allow free movement of sales people or we have a monopoly.",
        "fallacy_type": "false_dichotomy",
        "witness_statement": "I saw the defendant downloading the CRM database on Friday. He used his personal laptop. I was in the breakroom but I saw his screen from across the hall.",
        "contradictions": [
            {"description": "Screen visibility", "trigger_keywords": ["screen", "see", "hall"]},
            {"description": "Date of download", "trigger_keywords": ["friday", "when"]}
        ],
        "correct_argument_points": ["CRM data is non-public", "Targeted poaching evidence", "Breach of confidentiality"],
        "difficulty": "medium"
    },
    {
        "case_id": "CASE_007",
        "title": "Estate of Davis v. Care-Right Hospital",
        "facts": "The family of Davis claims medical malpractice led to his death. The hospital claims it was a known complication.",
        "area_of_law": "tort",
        "precedents": [
            {"name": "Patient v. Protocol", "summary": "Failure to follow standard diagnostic steps is malpractice.", "relevant": True},
            {"name": "Doctor v. Decision", "summary": "Medical professionals are not liable for honest errors in judgment.", "relevant": False},
            {"name": "Consent v. Risk", "summary": "Signed consent forms waive liability for known complications.", "relevant": False}
        ],
        "opposing_argument": "If we find the doctor liable here, every doctor in the country will stop performing surgeries for fear of being sued.",
        "fallacy_type": "slippery_slope",
        "witness_statement": "I checked the vitals at 10 PM and they were stable. I was at the nursing station. I didn't actually go into the room, but the monitor was blinking green.",
        "contradictions": [
            {"description": "Physical check vs monitor", "trigger_keywords": ["room", "inside", "monitor"]},
            {"description": "Vitals stability", "trigger_keywords": ["stable", "vitals"]}
        ],
        "correct_argument_points": ["Departure from standard protocol", "Ignored warning signs", "Direct link to outcome"],
        "difficulty": "medium"
    },
    {
        "case_id": "CASE_008",
        "title": "State v. Marcus",
        "facts": "Marcus is charged with arson of a competitor's warehouse. He has an alibi but it's his own brother.",
        "area_of_law": "criminal",
        "precedents": [
            {"name": "State v. Witness", "summary": "Alibi testimony from family requires corroborating physical evidence.", "relevant": False},
            {"name": "Fire v. Intent", "summary": "Arson requires proof of both actus reus and specific intent to destroy.", "relevant": True},
            {"name": "Brother v. Bond", "summary": "Immediate family members cannot be compelled to testify against siblings.", "relevant": False}
        ],
        "opposing_argument": "The defendant is a known troublemaker who dropped out of school, so he clearly has the character of an arsonist.",
        "fallacy_type": "ad_hominem",
        "witness_statement": "I saw a blue car speeding away from the warehouse at midnight. It looked exactly like Marcus's car. I was walking my cat and it was very quiet.",
        "contradictions": [
            {"description": "Vehicle identification in dark", "trigger_keywords": ["car", "blue", "see"]},
            {"description": "Time of sighting", "trigger_keywords": ["midnight", "when"]}
        ],
        "correct_argument_points": ["Lack of specific intent", "Inconclusive identification", "Circumstantial nature of evidence"],
        "difficulty": "medium"
    },
    {
        "case_id": "CASE_009",
        "title": "Riverside HOA v. Patel",
        "facts": "The HOA is suing Patel for painting his door 'electric blue', which they claim violates 'muted tones' rules.",
        "area_of_law": "property",
        "precedents": [
            {"name": "Color v. Community", "summary": "Aesthetic rules must be specifically defined to be enforceable.", "relevant": True},
            {"name": "Home v. Rule", "summary": "HOAs have broad authority to regulate the exterior appearance of homes.", "relevant": False},
            {"name": "Patel v. Board", "summary": "Failure to object within 30 days constitutes a waiver of the rule.", "relevant": False}
        ],
        "opposing_argument": "The HOA president says that 'electric blue' is a gateway color; soon everyone will be painting their houses neon pink.",
        "fallacy_type": "slippery_slope",
        "witness_statement": "I noticed the door on Tuesday morning. It was so bright it hurt my eyes. I was driving by at 40mph but it was unmistakable.",
        "contradictions": [
            {"description": "Observation while driving", "trigger_keywords": ["driving", "speed", "notice"]},
            {"description": "Subjective brightness", "trigger_keywords": ["bright", "eyes"]}
        ],
        "correct_argument_points": ["Vagueness of 'muted tones'", "Selective enforcement", "Lack of specific color list"],
        "difficulty": "medium"
    },
    {
        "case_id": "CASE_010",
        "title": "Dixon v. Best-Buy Autos",
        "facts": "Dixon bought a 'certified pre-owned' car that broke down the next day. The dealer cites the 'as-is' clause.",
        "area_of_law": "contract",
        "precedents": [
            {"name": "Lemon v. Dealer", "summary": "Implied warranty of merchantability overrides 'as-is' for certified cars.", "relevant": True},
            {"name": "Buyer v. Beware", "summary": "Oral promises by salespeople are superseded by written contracts.", "relevant": False},
            {"name": "Auto v. Failure", "summary": "Mechanical failure within 48 hours is presumed to be a pre-existing condition.", "relevant": False}
        ],
        "opposing_argument": "The plaintiff's lawyer claims this is fraud, but they basically want to eliminate the entire used car industry.",
        "fallacy_type": "straw_man",
        "witness_statement": "The car was in perfect condition during the test drive. I checked the engine personally on Wednesday. I'm not a mechanic, but I've owned cars for 20 years.",
        "contradictions": [
            {"description": "Expertise vs claim", "trigger_keywords": ["mechanic", "engine", "checked"]},
            {"description": "Date of inspection", "trigger_keywords": ["wednesday", "when"]}
        ],
        "correct_argument_points": ["Implied warranty applicability", "Misleading 'certified' label", "Pre-existing mechanical defect"],
        "difficulty": "medium"
    },

    # HARD CASES (Cross Examine)
    {
        "case_id": "CASE_011",
        "title": "State v. Sterling",
        "facts": "Sterling is accused of white-collar embezzlement. The star witness is the accountant who reported him.",
        "area_of_law": "criminal",
        "precedents": [
            {"name": "Audit v. Intent", "summary": "Accounting errors require proof of deceptive intent for criminal charges.", "relevant": True},
            {"name": "Finance v. Disclosure", "summary": "Failure to report offshore accounts is a strict liability offense.", "relevant": False},
            {"name": "State v. Ledger", "summary": "Digital logs are admissible only with a verified chain of custody.", "relevant": False}
        ],
        "opposing_argument": "Professor Higgins of the Global Ethics Board says Sterling is guilty, so we should move to sentencing.",
        "fallacy_type": "appeal_to_authority",
        "witness_statement": "I discovered the missing funds on Monday, March 3rd. I was working late in the office alone. I remember the date because it was my birthday, which is March 4th.",
        "contradictions": [
            {"description": "Date mismatch", "trigger_keywords": ["date", "monday", "march", "birthday"]},
            {"description": "Alone vs discovery", "trigger_keywords": ["alone", "discovered", "who"]}
        ],
        "correct_argument_points": ["Lack of deceptive intent", "Possible accounting error", "Witness credibility/date confusion"],
        "difficulty": "hard"
    },
    {
        "case_id": "CASE_012",
        "title": "Oakwood v. Pine Valley",
        "facts": "A dispute over a property line where Oakwood built a fence. Pine Valley claims the fence is 2 feet over.",
        "area_of_law": "property",
        "precedents": [
            {"name": "Survey v. Fence", "summary": "Official historical surveys take precedence over recent unofficial markers.", "relevant": True},
            {"name": "Marker v. Usage", "summary": "Long-term usage of a boundary creates a prescriptive easement.", "relevant": False},
            {"name": "Land v. Dispute", "summary": "Property disputes under $5,000 must be settled in small claims court.", "relevant": False}
        ],
        "opposing_argument": "You either agree that the fence must be moved immediately, or you admit you don't care about property rights at all.",
        "fallacy_type": "false_dichotomy",
        "witness_statement": "I used the original 1950 survey to set the markers. I did it at noon on a clear day. I couldn't find the original iron pin, so I guessed based on the oak tree.",
        "contradictions": [
            {"description": "Survey accuracy vs guessing", "trigger_keywords": ["guess", "iron pin", "survey"]},
            {"description": "Noon vs clear day", "trigger_keywords": ["noon", "visibility", "clear"]}
        ],
        "correct_argument_points": ["Reliance on unofficial markers", "Inaccuracy of the tree-based guess", "Priority of 1950 survey"],
        "difficulty": "hard"
    },
    {
        "case_id": "CASE_013",
        "title": "Fletcher v. Green-Grocers",
        "facts": "Fletcher slipped on a grape in the produce aisle. The store claims they sweep every 15 minutes.",
        "area_of_law": "tort",
        "precedents": [
            {"name": "Slip v. Notice", "summary": "Liability depends on whether the hazard existed for a 'reasonable' time.", "relevant": True},
            {"name": "Store v. Safety", "summary": "Constant sweeping logs are sufficient defense against slip-and-fall claims.", "relevant": False},
            {"name": "Grape v. Floor", "summary": "Produce spills are inherent risks assumed by shoppers.", "relevant": False}
        ],
        "opposing_argument": "The plaintiff is just a clumsy person who doesn't look where they are going, so the store isn't at fault.",
        "fallacy_type": "ad_hominem",
        "witness_statement": "I swept the grape aisle at 10:15 AM. I was very thorough. I was actually in the back room from 10:00 to 10:30, but I remember sweeping before I went in.",
        "contradictions": [
            {"description": "Time of sweep vs presence", "trigger_keywords": ["sweep", "time", "back room"]},
            {"description": "Thoroughness vs absence", "trigger_keywords": ["thorough", "how"]}
        ],
        "correct_argument_points": ["Failure of sweeping protocol", "Duration of hazard presence", "Constructive notice"],
        "difficulty": "hard"
    },
    {
        "case_id": "CASE_014",
        "title": "Baker v. Software-Solutions",
        "facts": "Baker claims his contract was breached when the software delivered was 3 months late. The company cites 'Force Majeure'.",
        "area_of_law": "contract",
        "precedents": [
            {"name": "Time v. Essence", "summary": "Delays are breaches if the contract specifies 'time is of the essence'.", "relevant": True},
            {"name": "Code v. Delay", "summary": "Software bugs are considered standard industry risks, not breaches.", "relevant": False},
            {"name": "Majeure v. Event", "summary": "Labor shortages do not qualify as Force Majeure events.", "relevant": False}
        ],
        "opposing_argument": "If we allow companies to be sued for late software, no one will ever start a tech company again.",
        "fallacy_type": "slippery_slope",
        "witness_statement": "The project was on track until the internet outage in February. The outage lasted for two weeks. I was able to work from home using my 5G hotspot the whole time though.",
        "contradictions": [
            {"description": "Outage vs work capability", "trigger_keywords": ["outage", "hotspot", "work"]},
            {"description": "Duration of delay", "trigger_keywords": ["two weeks", "delay", "february"]}
        ],
        "correct_argument_points": ["Time is of the essence clause", "Invalid force majeure claim", "Actual work capability during outage"],
        "difficulty": "hard"
    },
    {
        "case_id": "CASE_015",
        "title": "State v. Lawson",
        "facts": "Lawson is charged with burglary. He was found with the stolen goods in his trunk 2 hours later.",
        "area_of_law": "criminal",
        "precedents": [
            {"name": "Search v. Trunk", "summary": "Warrantless trunk searches require probable cause of a specific crime.", "relevant": True},
            {"name": "Burglary v. Possession", "summary": "Possession of stolen goods is not proof of the burglary itself.", "relevant": False},
            {"name": "Police v. Stop", "summary": "A broken taillight justifies a full vehicle search.", "relevant": False}
        ],
        "opposing_argument": "Lawson is either a thief who deserves prison, or you think it's okay for people to break into homes.",
        "fallacy_type": "false_dichotomy",
        "witness_statement": "I saw the defendant's car parked outside the house at 3 AM. It was pitch black and I was looking through a telescope from two blocks away. I saw his face clearly.",
        "contradictions": [
            {"description": "Visibility through telescope in dark", "trigger_keywords": ["telescope", "dark", "see", "face"]},
            {"description": "Location of car", "trigger_keywords": ["parked", "where"]}
        ],
        "correct_argument_points": ["Invalid search of trunk", "Insufficient proof of entry", "Unreliable witness identification"],
        "difficulty": "hard"
    }
]
