abstract public class Expr {
    abstract <R> R accept(Visitor<R> visitor);
    interface Visitor<R> {
        R visitBinaryExpr(Binary expr);
        R visitGroupingExpr(Grouping expr);
        R visitLiteralExpr(Literal expr);
        R visitUnaryExpr(Unary expr);
        R visitVariableExpr(Variable expr);
    }

    static class Variable extends Expr {
        final Token name;

        Variable(Token name) {
            this.name = name;
        }

        <R> R accept(Visitor<R> visitor) {
            return visitor.visitVariableExpr(this);
        }
    }
    static class Binary extends Expr {
        final Expr left;
        final Token operator;
        final Expr right;

        <R> R accept(Visitor<R> visitor) {
            return visitor.visitBinaryExpr(this);
        }

        Binary(Expr left, Token operator, Expr right) {
            this.left = left;
            this.operator = operator;
            this.right = right;
        }

        public String toString() {
            return String.format("Binary(%s, %s, %s)",
                    left,
                    operator,
                    right);
        }
    }

    static class Grouping extends Expr {
        final Expr expression;

        <R> R accept(Visitor<R> visitor) {
            return visitor.visitGroupingExpr(this);
        }
        Grouping(Expr expression) {
            this.expression = expression;
        }
    }

    static class Literal extends Expr {
        final Object value;

        <R> R accept(Visitor<R> visitor) {
            return visitor.visitLiteralExpr(this);
        }
        Literal(Object value) {
            this.value = value;
        }

        @Override
        public String toString() {
            return String.format("Literal(%s)", value.toString());
        }
    }

    static class Unary extends Expr {
        final Token operator;
        final Expr right;

        <R> R accept(Visitor<R> visitor) {
            return visitor.visitUnaryExpr(this);
        }

        Unary(Token operator, Expr right) {
            this.operator = operator;
            this.right = right;
        }
    }
}