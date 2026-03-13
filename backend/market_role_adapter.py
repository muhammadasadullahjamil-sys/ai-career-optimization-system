from typing import List, Dict, Optional


class MarketRoleAdapter:
    """
    Responsible ONLY for transforming resume-extracted roles
    into clean, canonical, market-searchable job titles.
    """

    # Canonical role mapping
    # Maps known variations to standardized market titles.
    ROLE_CANONICAL_MAP: Dict[str, str] = {
        # =====================================================
        # UX / DESIGN
        # =====================================================

        "ux designer": "UX Designer",
        "user experience designer": "UX Designer",
        "ui/ux designer": "UX Designer",
        "ux/ui designer": "UX Designer",
        "user interface designer": "UI Designer",
        "ui designer": "UI Designer",
        "product designer": "Product Designer",
        "digital product designer": "Product Designer",
        "interaction designer": "Interaction Designer",
        "visual designer": "Visual Designer",
        "graphic designer": "Graphic Designer",
        "motion designer": "Motion Designer",
        "brand designer": "Brand Designer",
        "design researcher": "UX Researcher",
        "ux researcher": "UX Researcher",
        "service designer": "Service Designer",
        "experience designer": "UX Designer",
        "design lead": "Design Lead",
        "head of design": "Design Director",
        "design director": "Design Director",
        "creative director": "Creative Director",

        # =====================================================
        # SOFTWARE ENGINEERING
        # =====================================================

        "software engineer": "Software Engineer",
        "software developer": "Software Engineer",
        "application developer": "Software Engineer",
        "programmer": "Software Engineer",
        "backend engineer": "Backend Engineer",
        "backend developer": "Backend Engineer",
        "frontend engineer": "Frontend Engineer",
        "frontend developer": "Frontend Engineer",
        "front end developer": "Frontend Engineer",
        "back end developer": "Backend Engineer",
        "full stack developer": "Full Stack Engineer",
        "full stack engineer": "Full Stack Engineer",
        "web developer": "Web Developer",
        "web engineer": "Web Developer",
        "mobile developer": "Mobile Developer",
        "ios developer": "iOS Developer",
        "android developer": "Android Developer",
        "embedded software engineer": "Embedded Engineer",
        "systems engineer": "Systems Engineer",
        "application engineer": "Software Engineer",
        "platform engineer": "Platform Engineer",
        "site reliability engineer": "Site Reliability Engineer",
        "sre": "Site Reliability Engineer",
        "devops engineer": "DevOps Engineer",
        "cloud engineer": "Cloud Engineer",
        "cloud developer": "Cloud Engineer",
        "infrastructure engineer": "Infrastructure Engineer",
        "release engineer": "Release Engineer",
        "build engineer": "Build Engineer",

        # =====================================================
        # DATA & AI
        # =====================================================

        "data scientist": "Data Scientist",
        "machine learning engineer": "Machine Learning Engineer",
        "ml engineer": "Machine Learning Engineer",
        "ai engineer": "AI Engineer",
        "artificial intelligence engineer": "AI Engineer",
        "data analyst": "Data Analyst",
        "business intelligence analyst": "BI Analyst",
        "bi analyst": "BI Analyst",
        "data engineer": "Data Engineer",
        "analytics engineer": "Analytics Engineer",
        "research scientist": "Research Scientist",
        "nlp engineer": "NLP Engineer",
        "computer vision engineer": "Computer Vision Engineer",
        "deep learning engineer": "Deep Learning Engineer",
        "statistician": "Statistician",
        "quantitative analyst": "Quantitative Analyst",
        "data architect": "Data Architect",
        "ai researcher": "AI Researcher",
        "ml researcher": "ML Researcher",

        # =====================================================
        # PRODUCT & MANAGEMENT
        # =====================================================

        "product manager": "Product Manager",
        "technical product manager": "Technical Product Manager",
        "associate product manager": "Product Manager",
        "product owner": "Product Owner",
        "project manager": "Project Manager",
        "technical project manager": "Technical Project Manager",
        "program manager": "Program Manager",
        "delivery manager": "Delivery Manager",
        "scrum master": "Scrum Master",
        "agile coach": "Agile Coach",
        "portfolio manager": "Portfolio Manager",
        "operations manager": "Operations Manager",

        # =====================================================
        # BUSINESS & ANALYTICS
        # =====================================================

        "business analyst": "Business Analyst",
        "strategy analyst": "Strategy Analyst",
        "operations analyst": "Operations Analyst",
        "management consultant": "Management Consultant",
        "consultant": "Consultant",
        "financial analyst": "Financial Analyst",
        "investment analyst": "Investment Analyst",
        "risk analyst": "Risk Analyst",
        "supply chain analyst": "Supply Chain Analyst",
        "process analyst": "Process Analyst",
        "systems analyst": "Systems Analyst",

        # =====================================================
        # MARKETING & GROWTH
        # =====================================================

        "marketing manager": "Marketing Manager",
        "digital marketing manager": "Digital Marketing Manager",
        "growth manager": "Growth Manager",
        "growth hacker": "Growth Manager",
        "seo specialist": "SEO Specialist",
        "content marketer": "Content Marketing Specialist",
        "content strategist": "Content Strategist",
        "social media manager": "Social Media Manager",
        "performance marketer": "Performance Marketing Manager",
        "brand manager": "Brand Manager",
        "product marketing manager": "Product Marketing Manager",
        "email marketing specialist": "Email Marketing Specialist",

        # =====================================================
        # SALES
        # =====================================================

        "sales manager": "Sales Manager",
        "account manager": "Account Manager",
        "business development manager": "Business Development Manager",
        "sales executive": "Sales Executive",
        "account executive": "Account Executive",
        "customer success manager": "Customer Success Manager",
        "customer success specialist": "Customer Success Specialist",
        "sales representative": "Sales Representative",

        # =====================================================
        # FINANCE
        # =====================================================

        "accountant": "Accountant",
        "chartered accountant": "Accountant",
        "auditor": "Auditor",
        "finance manager": "Finance Manager",
        "controller": "Financial Controller",
        "cfo": "Chief Financial Officer",
        "chief financial officer": "Chief Financial Officer",
        "tax analyst": "Tax Analyst",
        "investment banker": "Investment Banker",

        # =====================================================
        # HR
        # =====================================================

        "hr manager": "HR Manager",
        "human resources manager": "HR Manager",
        "talent acquisition specialist": "Talent Acquisition Specialist",
        "recruiter": "Recruiter",
        "technical recruiter": "Technical Recruiter",
        "people operations manager": "People Operations Manager",

        # =====================================================
        # CYBERSECURITY
        # =====================================================

        "security engineer": "Security Engineer",
        "cybersecurity engineer": "Security Engineer",
        "information security analyst": "Security Analyst",
        "security analyst": "Security Analyst",
        "penetration tester": "Penetration Tester",
        "ethical hacker": "Penetration Tester",
        "security architect": "Security Architect",
        "soc analyst": "Security Operations Analyst",

        # =====================================================
        # CLOUD & DEVOPS
        # =====================================================

        "aws engineer": "Cloud Engineer",
        "azure engineer": "Cloud Engineer",
        "gcp engineer": "Cloud Engineer",
        "kubernetes engineer": "Platform Engineer",
        "terraform engineer": "DevOps Engineer",
        "cloud architect": "Cloud Architect",

        # =====================================================
        # QA / TESTING
        # =====================================================

        "qa engineer": "QA Engineer",
        "quality assurance engineer": "QA Engineer",
        "test engineer": "Test Engineer",
        "automation engineer": "Automation Engineer",
        "software tester": "QA Engineer",

        # =====================================================
        # HEALTHCARE
        # =====================================================

        "doctor": "Physician",
        "physician": "Physician",
        "registered nurse": "Registered Nurse",
        "nurse practitioner": "Nurse Practitioner",
        "pharmacist": "Pharmacist",
        "medical assistant": "Medical Assistant",
        "clinical researcher": "Clinical Researcher",

        # =====================================================
        # ENGINEERING (NON-SOFTWARE)
        # =====================================================

        "mechanical engineer": "Mechanical Engineer",
        "electrical engineer": "Electrical Engineer",
        "civil engineer": "Civil Engineer",
        "chemical engineer": "Chemical Engineer",
        "industrial engineer": "Industrial Engineer",
        "manufacturing engineer": "Manufacturing Engineer",
        "quality engineer": "Quality Engineer",

        # =====================================================
        # EXECUTIVE
        # =====================================================

        "ceo": "Chief Executive Officer",
        "chief executive officer": "Chief Executive Officer",
        "cto": "Chief Technology Officer",
        "chief technology officer": "Chief Technology Officer",
        "coo": "Chief Operating Officer",
        "chief operating officer": "Chief Operating Officer",
        "vp engineering": "VP Engineering",
        "vp product": "VP Product",
    }

    # -----------------------------------------------------
    # INTERNAL UTILITIES
    # -----------------------------------------------------

    @staticmethod
    def _clean(role: str) -> str:
        """
        Basic whitespace normalization.
        """
        return " ".join(role.strip().split())

    @classmethod
    def _canonicalize(cls, role: str) -> str:
        """
        Converts role to canonical market title if known.
        Otherwise, returns title-cased version.
        """
        role_lower = role.lower()

        return cls.ROLE_CANONICAL_MAP.get(role_lower, role.title())

    # -----------------------------------------------------
    # PUBLIC API
    # -----------------------------------------------------

    @classmethod
    def normalize_single(cls, role: str) -> Optional[str]:
        """
        Normalize a single role into canonical format.
        """

        if not role or not isinstance(role, str):
            return None

        role = cls._clean(role)

        if not role:
            return None

        return cls._canonicalize(role)

    @classmethod
    def normalize_roles(cls, roles: List[str]) -> List[str]:
        """
        Normalize multiple roles.
        - Cleans each role
        - Canonicalizes
        - Removes duplicates (preserves order)
        - Limits output to maximum 3 roles
        """

        if not roles:
            return []

        normalized_roles = []

        for role in roles:
            normalized = cls.normalize_single(role)
            if normalized:
                normalized_roles.append(normalized)

        # Deduplicate while preserving order
        seen = set()
        unique_roles = []
        for role in normalized_roles:
            if role not in seen:
                seen.add(role)
                unique_roles.append(role)

        return unique_roles[:3]

    @staticmethod
    def prepare_for_query(role: str) -> str:
        """
        Convert canonical role to search-ready keyword.
        Example:
            "UX Designer" -> "ux designer"
        """
        if not role:
            return ""

        return role.lower().strip()
