class Player:
    def __init__(self):
        self._balance = 50.0
        self._deliveries_completed = 0
        self._lawyers = 0
        self._current_job = None
        self._jailed = False
        self._dead = False

    @property
    def balance(self):
        return self._balance

    @property
    def deliveries_completed(self):
        return self._deliveries_completed

    @property
    def lawyers(self):
        return self._lawyers

    @property
    def current_job(self):
        return self._current_job

    @property
    def jailed(self):
        return self._jailed

    @property
    def dead(self):
        return self._dead

    @property
    def quality(self):
        return min(self.deliveries_completed / 10, 1.0)

    def earn(self, amount):
        if amount < 0:
            raise ValueError("O valor recebido não pode ser negativo")
        self._balance += amount

    def spend(self, amount):
        if amount < 0:
            raise ValueError("O valor gasto não pode ser negativo")
        if amount > self.balance:
            return False
        self._balance -= amount
        return True

    def complete_delivery(self):
        self._deliveries_completed += 1

    def hire_lawyer(self, cost):
        if not self.spend(cost):
            return False
        self._lawyers += 1
        return True

    def apply_for_job(self, job):
        if self.jailed or self.dead:
            return False
        if self.current_job is not None:
            return False
        if not job.can_apply(self):
            return False
        if not job.accept():
            return False
        self._current_job = job
        return True

    def complete_job(self):
        if self.current_job is None:
            return False

        job = self.current_job
        job.complete(self)
        self._current_job = None
        return True

    def jail(self):
        self._jailed = True
        self._current_job = None

    def serve_sentence(self):
        if not self.jailed:
            return False

        self._jailed = False
        return True

    def die(self):
        self._dead = True
        self._jailed = False
        self._current_job = None
