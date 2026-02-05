# botish

### Запуск брокера очередей
```
taskiq worker botish.tasks.broker:broker botish.tasks.tasks
```

### Запуск планировщика
```
taskiq scheduler botish.tasks.scheduler:scheduler botish.tasks.tasks
```