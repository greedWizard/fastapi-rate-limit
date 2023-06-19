FETCH_RESPONSES_DATA_SQL = '''
SELECT responded_at, status_code, COUNT(responses.status_code)
FROM responses
WHERE url = :url
GROUP BY responded_at, status_code
ORDER BY responded_at DESC
LIMIT :limit
OFFSET :offset
;
'''