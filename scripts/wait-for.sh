#!/usr/bin/env bash
# wait-for.sh

set -e

HOST_PORT="$1"
shift
CMD="$@"

host=$(echo $HOST_PORT | cut -d: -f1)
port=$(echo $HOST_PORT | cut -d: -f2)

echo "⏳ Aguardando $host:$port..."

# tenta conexão até liberar
while ! nc -z $host $port; do
  sleep 1
done

echo "✅ $host:$port está pronto!"

# executa o comando passado após o "--"
exec $CMD
