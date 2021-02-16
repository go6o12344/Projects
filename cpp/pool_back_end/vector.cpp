class vec2{
	public:
		double x, y;
		vec2(double x,double y)x{x}, y{y}{}
		vec2& add(vec2& v){
			this->x += v->x;
			this->y += v->y;
			return *this;
		}
		vec2& multiply(double t){
			this->x *= t;
			this->y *= t;
			return *this;
		}
		int dotProduct(vec2& v){
			return this->x * v->x + this->y * v->y;
		}
		vec2& sub(vec2& v){
			this->x -= v->x;
			this->y -= v->y;
			return *this;
		}
		
};