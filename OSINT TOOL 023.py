import asyncio
import httpx

class Finding:
    def __init__(self, module, claim, confidence, evidence, links, risk_points, attacker_note):
        self.module = module
        self.claim = claim
        self.confidence = confidence
        self.evidence = evidence
        self.links = links
        self.risk_points = risk_points
        self.attacker_note = attacker_note

class ColdReadModule:
    async def run(self, username):
        platforms = [
            f"https://github.com/{username}",
            f"https://twitter.com/{username}",
            f"https://instagram.com/{username}",
            f"https://reddit.com/user/{username}"
        ]
        found = []
        async with httpx.AsyncClient(timeout=5.0, follow_redirects=True) as client:
            for url in platforms:
                try:
                    response = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
                    if response.status_code == 200:
                        found.append(url)
                except httpx.RequestError:
                    pass
        
        confidence = "Certain (85%)" if len(found) > 2 else "Suspicion (50%)"
        return Finding(
            module="Cold Read",
            claim=f"Reuses the handle on {len(found)} platforms",
            confidence=confidence,
            evidence=found,
            links=found,
            risk_points=24,
            attacker_note="Link other accounts and build a social-engineering profile."
        )

async def main():
    username = "alex_marlowe"
    module = ColdReadModule()
    result = await module.run(username)
    print(f"Module: {result.module}")
    print(f"Claim: {result.claim}")
    print(f"Confidence: {result.confidence}")
    print(f"Evidence: {result.evidence}")
    print(f"Risk Points: {result.risk_points}")
    print(f"Attacker Note: {result.attacker_note}")

if __name__ == "__main__":
    asyncio.run(main())
