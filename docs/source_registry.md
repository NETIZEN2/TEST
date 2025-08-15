# Source Registry

| Source | Terms of Service | Auth | Endpoint | Limits | Retention TTL | Permitted Uses | Review Cadence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Wikipedia API | [API:TOS](https://www.mediawiki.org/wiki/API:Main_page) | none | `/w/api.php` | polite usage | 180 days | research, citation | annual |
| Google News RSS | [Google ToS](https://policies.google.com/terms) | none | `/rss` | Google rate limits | 180 days | media monitoring | annual |
| RDAP | [rdap.org](https://rdap.org/) | none | `/domain/` | per-registry | 180 days | domain research | annual |
| GitHub Users API | [GitHub ToS](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service) | none | `/users/{user}` | 60 req/min | 180 days | open-source attribution | annual |
| SEC EDGAR | [SEC access](https://www.sec.gov/os/accessing-edgar-data) | none | `/Archives/edgar/data/` | as published | 180 days | corporate filings | annual |
| Companies House | [CH API Terms](https://developer.company-information.service.gov.uk/terms-and-conditions) | API key | `/company/{id}` | 600 req/5min | 180 days | UK registry checks | annual |
| OpenCorporates | [Terms](https://api.opencorporates.com/documentation/API-Reference) | API key | `/companies/search` | 1000/day | 180 days | global registry checks | annual |
| GDELT | [GDELT Terms](https://www.gdeltproject.org/about.html) | none | `/api/v2/events` | as published | 180 days | event analysis | annual |
| crt.sh | [crt.sh](https://crt.sh/) | none | `/?q=` | fair use | 180 days | certificate lookups | annual |
| Wayback Machine | [IA Terms](https://archive.org/about/terms.php) | none | `/wayback/available` | polite usage | 180 days | historical snapshots | annual |
| OpenAlex | [OpenAlex ToS](https://docs.openalex.org/terms) | none | `/works` | 100k/day | 180 days | scholarly analysis | annual |
| Wikidata | [Wikidata ToS](https://www.wikidata.org/wiki/Wikidata:Data_access) | none | `/w/api.php` | polite usage | 180 days | knowledge graph enrichment | annual |

List of data sources and their provenance.

- **Wikipedia API** – <https://www.mediawiki.org/wiki/API:Main_page>
- **Google News RSS** – <https://news.google.com/rss> (usage subject to Google Terms of Service)
- **RDAP** – <https://rdap.org/> (open registration data)
- **GitHub Users API** – <https://docs.github.com/en/rest/users/users> (subject to GitHub Terms of Service)
- **SEC EDGAR** – <https://www.sec.gov/os/accessing-edgar-data> (open corporate filings; rate limits apply)
- **Companies House API** – <https://developer.company-information.service.gov.uk/> (UK corporate registry)
- **OpenCorporates** – <https://api.opencorporates.com/> (subject to OpenCorporates Terms of Use)
- **GDELT Project** – <https://www.gdeltproject.org/> (open news events data)
- **Certificate Transparency Logs (crt.sh)** – <https://crt.sh/> (public certificate logs)
- **Wayback Machine** – <https://archive.org/> (subject to Internet Archive Terms of Use)
- **OpenAlex** – <https://openalex.org/> (open scholarly data)
- **Wikidata** – <https://www.wikidata.org/wiki/Wikidata:Data_access> (CC0 data)
