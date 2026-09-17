Use the Python SDK when a worker needs explicit status, result, or cancellation control for an existing request. The TypeScript v2 client currently exposes automatic polling through `subscribe`.

```python
import higgsfield_client

request_id = "{request_id}"
status = higgsfield_client.status(request_id=request_id)
result = higgsfield_client.result(request_id=request_id)
higgsfield_client.cancel(request_id=request_id)
```

## Additional Resources

- [Model page](https://console.higgsfield.ai/models/bytedance/seedance-2.5/reference-to-video)
- [This LLM-readable document](http://dash.higgsfield.ai/models/bytedance/seedance-2.5/reference-to-video/llms.txt)

## Documentation Index

- [Complete Higgsfield documentation](https://docs.higgsfield.ai/docs/llms.txt)
