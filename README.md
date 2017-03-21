# spellbound

### Produce schema from endpoint
```
curl test.com | spellbound > schema.json
```

### Diff endpoint against schema
```
curl test.com | spellbound -s schema.json > diff.json
```
